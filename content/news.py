"""
News module. Pulls from a curated set of RSS/Atom feeds — Google News RSS
queries as the broad backbone, plus authoritative GOV.UK organisation
feeds — and serves a cached list of items per category.

Design notes:
- One module-level in-memory cache keyed by category.
- A background daemon thread refreshes every `REFRESH_SECONDS` so page
  renders never block on upstream fetches. First request after cold-start
  may see an empty list (we hide the section in that case).
- Per-feed fetch timeout is aggressive (6s) so a slow feed can't hold up
  the whole refresh. Per-feed failures are silently dropped.
"""

from __future__ import annotations

import html
import json
import os
import re
import socket
import threading
import time
from datetime import datetime, timezone
from typing import Any

import feedparser

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    import httpx
except ImportError:  # pragma: no cover
    httpx = None  # type: ignore


# ---------------------------------------------------------------------------
# Feed catalogue
# ---------------------------------------------------------------------------

# Google News RSS is a consistent, well-formed source of aggregated headlines
# across any topic. GOV.UK organisation .atom feeds are the authoritative
# channel for UK government announcements.
_GNEWS = "https://news.google.com/rss/search?hl=en-GB&gl=GB&ceid=GB:en&q="

FEEDS: dict[str, list[tuple[str, str]]] = {
    "ai": [
        ("Google News · AI in public services",
         _GNEWS + "%22artificial+intelligence%22+%22public+sector%22+OR+government+when:14d"),
        ("Google News · EU AI Act & regulation",
         _GNEWS + "%22EU+AI+Act%22+OR+%22AI+regulation%22+Europe+when:30d"),
        ("Google News · Generative AI enterprise",
         _GNEWS + "%22generative+AI%22+enterprise+deployment+when:14d"),
    ],
    "defense": [
        ("Google News · Defence + AI",
         _GNEWS + "defence+AI+procurement+UK+OR+NATO+OR+Europe+when:30d"),
        ("GOV.UK · Ministry of Defence",
         "https://www.gov.uk/government/organisations/ministry-of-defence.atom"),
        ("Google News · EU defence procurement",
         _GNEWS + "%22European+Defence+Fund%22+OR+%22EU+defence+procurement%22+when:45d"),
    ],
    "healthcare": [
        ("Google News · NHS AI & digital health",
         _GNEWS + "NHS+AI+OR+%22digital+health%22+UK+when:14d"),
        ("GOV.UK · Dept of Health & Social Care",
         "https://www.gov.uk/government/organisations/department-of-health-and-social-care.atom"),
        ("Google News · European health data",
         _GNEWS + "%22European+Health+Data+Space%22+OR+%22health+data%22+EU+AI+when:30d"),
    ],
    "public": [
        ("Google News · UK public sector digital",
         _GNEWS + "%22UK+public+sector%22+digital+OR+procurement+AI+when:14d"),
        ("GOV.UK · Central Digital & Data Office",
         "https://www.gov.uk/government/organisations/central-digital-and-data-office.atom"),
        ("GOV.UK · Cabinet Office",
         "https://www.gov.uk/government/organisations/cabinet-office.atom"),
        ("Google News · Local government AI",
         _GNEWS + "%22local+government%22+AI+UK+OR+Europe+when:30d"),
    ],
    "financial": [
        ("Google News · Financial services + AI",
         _GNEWS + "%22financial+services%22+AI+regulation+UK+OR+FCA+when:14d"),
        ("Google News · FinTech AI Europe",
         _GNEWS + "FinTech+AI+Europe+when:14d"),
    ],
}

# The home page composes a mixed feed from the top of each category.
HOME_MIX_ORDER = ["ai", "public", "healthcare", "defense", "financial"]


# ---------------------------------------------------------------------------
# Cache + refresher
# ---------------------------------------------------------------------------

REFRESH_SECONDS = 60 * 60  # 1 hour
FETCH_TIMEOUT_SECONDS = 6
MAX_ITEMS_PER_FEED = 10  # oversample; the relevance filter drops most admin noise
MAX_ITEMS_PER_CATEGORY = 6
MAX_ITEMS_HOME = 8

_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "PredictiveLabs-NewsFetcher/1.0"
)

_cache: dict[str, list[dict[str, Any]]] = {k: [] for k in FEEDS}
_cache["home"] = []
_cache_lock = threading.Lock()
_last_refresh = 0.0


def _parse_entry(source_label: str, entry: Any) -> dict[str, Any] | None:
    title = (entry.get("title") or "").strip()
    link = entry.get("link") or ""
    if not title or not link:
        return None
    published_struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if published_struct:
        try:
            published = datetime(*published_struct[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError):
            published = None
    else:
        published = None
    return {
        "title": html.unescape(title),
        "url": link,
        "source": source_label,
        "published": published,
    }


def _fetch_feed(source_label: str, url: str) -> list[dict[str, Any]]:
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(FETCH_TIMEOUT_SECONDS)
    try:
        parsed = feedparser.parse(url, agent=_USER_AGENT)
    except Exception:
        return []
    finally:
        socket.setdefaulttimeout(old_timeout)

    out: list[dict[str, Any]] = []
    for entry in (parsed.entries or [])[:MAX_ITEMS_PER_FEED]:
        item = _parse_entry(source_label, entry)
        if item:
            out.append(item)
    return out


def _dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = item["title"].lower()[:120]
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _sort_by_recency(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    undated_pos = len(items)

    def key(item):
        p = item.get("published")
        if p is None:
            nonlocal undated_pos
            undated_pos -= 1
            return (0, undated_pos)
        return (1, p.timestamp())

    return sorted(items, key=key, reverse=True)


# ---------------------------------------------------------------------------
# Relevance filter
# ---------------------------------------------------------------------------
#
# Raw feeds carry a lot of noise for our audience: admin notices, accessibility
# statements, "how to use these guidelines" stubs, historical fatality
# investigations, routine clinical-treatment protocols, etc. We filter in two
# passes:
#   1. Keyword fallback (no API required) — drops obvious admin noise.
#   2. LLM classifier via OpenRouter — keeps items that are public tenders,
#      sector AI/digital trends, regulatory news, or major sector-specific
#      developments; drops the rest.
# Classification results are cached by URL so each item is only classified
# once across refresh cycles.

_DROP_PATTERNS = [
    r"accessibility\s+statement",
    r"how\s+to\s+use\s+(these|this|the)\s+guidelines?",
    r"terms?\s+of\s+reference",
    r"fatality\s+investigation",
    r"investigation\s+into\s+the\s+deaths?",
    r"clinical\s+guidelines?\s+for\s+alcohol",
    r"\bcorrigendum\b",
    r"\bgsc\b.*accessibility",
    r"privacy\s+notice",
    r"cookie\s+policy",
    r"guidance\s*[:：].*(guideline|statement|privacy|cookie)",
]
_DROP_RE = re.compile("|".join(_DROP_PATTERNS), re.IGNORECASE)


def _keyword_drop(title: str) -> bool:
    return bool(_DROP_RE.search(title or ""))


# url -> (bool, tag)
_classify_cache: dict[str, tuple[bool, str]] = {}
_classify_lock = threading.Lock()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.environ.get("NEWS_FILTER_MODEL", "anthropic/claude-haiku-4-5")

_FILTER_PROMPT = """You filter a news feed for Predictive Labs, a consultancy that builds AI for European public services — defense, health, public management and mobility, financial services, and sector trends in AI and energy.

For each numbered item, decide if it is RELEVANT for our buyers (senior programme owners, procurement leads, technical directors in European public bodies and regulated enterprises).

KEEP items that are:
- Public tenders, procurement notices, framework agreements, or contract awards
- AI policy or regulation (EU AI Act, GDPR updates, national AI strategies, sovereign AI funding)
- Sector trends or AI deployments in health / defense / energy / education / public management / financial services
- Major product launches, partnerships, or research affecting these sectors
- Data releases, benchmarks, or open-source initiatives relevant to public-sector AI

DROP items that are:
- Administrative notices (accessibility statements, "how to use these guidelines", privacy notices, cookie policies, corrigenda)
- Historical fatality investigations, inquiries or case reviews unrelated to current AI / digital trends
- Clinical treatment protocols that are not about digital transformation, AI, or data
- Internal civil-service HR or procedure items
- Celebrity, entertainment, sports or unrelated political drama
- Generic marketing, PR fluff, sponsorship news

Tag each kept item with one short label from: tender, ai, health, defense, energy, public, financial, regulation, research.

Respond with JSON only, in this exact shape:
{"decisions": [{"i": 0, "keep": true, "tag": "ai"}, {"i": 1, "keep": false, "tag": "drop"}]}

Items:
"""


def _llm_classify(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Classify items via OpenRouter. Returns the list filtered to
    decisions==keep. On any failure or missing key, returns the input
    unchanged (fail-open)."""
    if not items or httpx is None:
        return items
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return items

    with _classify_lock:
        cached_decisions: dict[int, bool] = {}
        to_classify: list[tuple[int, dict[str, Any]]] = []
        for idx, it in enumerate(items):
            entry = _classify_cache.get(it["url"])
            if entry is not None:
                cached_decisions[idx] = entry[0]
            else:
                to_classify.append((idx, it))

    if not to_classify:
        return [it for idx, it in enumerate(items) if cached_decisions.get(idx, True)]

    numbered = "\n".join(
        f"{k}. [{it['source']}] {it['title']}" for k, (_, it) in enumerate(to_classify)
    )

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": _FILTER_PROMPT + numbered},
        ],
        "temperature": 0,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"},
    }

    try:
        resp = httpx.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://predictivelabs.ai",
                "X-Title": "Predictive Labs News Filter",
            },
            json=payload,
            timeout=20.0,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        decisions = data.get("decisions") if isinstance(data, dict) else data
        if not isinstance(decisions, list):
            return items
    except Exception:
        return items

    # Merge classifier decisions into cache
    with _classify_lock:
        for d in decisions:
            k = d.get("i")
            if not isinstance(k, int) or k < 0 or k >= len(to_classify):
                continue
            keep = bool(d.get("keep"))
            tag = str(d.get("tag", "") or "")
            idx, it = to_classify[k]
            _classify_cache[it["url"]] = (keep, tag)
            cached_decisions[idx] = keep

    # Any classifier entries missing from the response default to keep.
    return [
        it for idx, it in enumerate(items)
        if cached_decisions.get(idx, True)
    ]


def _filter(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not items:
        return items
    cheap = [it for it in items if not _keyword_drop(it.get("title", ""))]
    return _llm_classify(cheap)


def _refresh_category(key: str) -> list[dict[str, Any]]:
    gathered: list[dict[str, Any]] = []
    for source_label, url in FEEDS.get(key, []):
        gathered.extend(_fetch_feed(source_label, url))
    gathered = _dedupe(gathered)
    gathered = _filter(gathered)
    gathered = _sort_by_recency(gathered)
    return gathered[:MAX_ITEMS_PER_CATEGORY]


def _build_home_mix() -> list[dict[str, Any]]:
    mixed: list[dict[str, Any]] = []
    for cat in HOME_MIX_ORDER:
        for item in _cache.get(cat, [])[:2]:
            mixed.append(item)
    mixed = _dedupe(mixed)
    return mixed[:MAX_ITEMS_HOME]


def refresh_all():
    global _last_refresh
    for key in FEEDS:
        items = _refresh_category(key)
        with _cache_lock:
            _cache[key] = items
    with _cache_lock:
        _cache["home"] = _build_home_mix()
        _last_refresh = time.time()


def _refresher_loop():
    while True:
        try:
            refresh_all()
        except Exception:
            pass
        time.sleep(REFRESH_SECONDS)


def start_background_refresh():
    """Kick off a daemon thread that refreshes the cache every hour.
    Safe to call multiple times — only the first call spawns the thread."""
    if getattr(start_background_refresh, "_started", False):
        return
    start_background_refresh._started = True
    t = threading.Thread(target=_refresher_loop, daemon=True, name="news-refresher")
    t.start()


def items_for(category: str) -> list[dict[str, Any]]:
    with _cache_lock:
        return list(_cache.get(category, []))


def last_refresh_iso() -> str | None:
    if _last_refresh <= 0:
        return None
    return datetime.fromtimestamp(_last_refresh, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def format_published(p: datetime | None, *, lang: str = "en") -> str:
    if p is None:
        return ""
    from utils.i18n import t as _t
    now = datetime.now(tz=timezone.utc)
    delta = now - p
    hours = int(delta.total_seconds() // 3600)
    if hours < 1:
        return _t("time_just_now", lang)
    if hours < 24:
        return _t("time_hours_ago", lang).replace("{n}", str(hours))
    days = hours // 24
    if days < 7:
        return _t("time_days_ago", lang).replace("{n}", str(days))
    return p.strftime("%d %b %Y")
