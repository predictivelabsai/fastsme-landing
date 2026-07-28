"""
Predictive Labs — multipage FastHTML landing site (v2).

Dark, palantir-inspired, public-sector first. Content lives in content/*.py;
routes are thin composition layers over components.py primitives.
"""

from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from fasthtml.common import (
    fast_app, serve, Div, Span, A, P, Ul, Li, Section, Article, Header,
    NotStr, Script, Style, H1, H2, H3, Button,
)

from components import (
    page, Hero, Pillar, MetricTile, CaseStudyCard, CTASection, NewsSection,
    Section_, Heading, Eyebrow, Pill, Button_, SectorLink,
    CONTACT_EMAIL, GITHUB_URL, LINKEDIN_URL,
)
from content.case_studies import ALL as ALL_CASES, BID_DERIVED, NAMED_PRECEDENTS
from content.team import TEAM
from content.repos import REPOS, EXTERNAL_RESEARCH, APP_SUITE
from content import signal as signal_mod
from content import news as news_mod
from utils.i18n import t, get_lang, set_lang

# Kick off the background RSS refresher once at import time so page renders
# never block on upstream fetches.
news_mod.start_background_refresh()


app, rt = fast_app(live=False, static_path=".", pico=False, secret_key="plai-landing-sess-2026")


def _lang(request: Request) -> str:
    return get_lang(request.session, request)


@rt("/lang", methods=["POST"])
async def lang_switch(request: Request):
    form = await request.form()
    code = (form.get("lang") or "").strip()
    if code:
        set_lang(request.session, code)
    return JSONResponse({"ok": True})


# ---------- /  Home ----------

@rt("/")
def home(request: Request):
    lang = _lang(request)
    pillars = [
        ("01", t("pillar_doc_intel", lang), t("pillar_doc_intel_body", lang)),
        ("02", t("pillar_forecasting", lang), t("pillar_forecasting_body", lang)),
        ("03", t("pillar_geo", lang), t("pillar_geo_body", lang)),
        ("04", t("pillar_agents", lang), t("pillar_agents_body", lang)),
    ]

    logos_row = [
        "Microsoft (ISD)", "ARM Holdings", "DBRS Morningstar", "London Stock Exchange Group",
        "Nando's", "Indurent (Blackstone)",
    ]

    home_cases = [c for c in ALL_CASES if c["id"] in ("uk-traffic-od", "nordic-health-rwd", "microsoft-isd")]

    return page(
        t("home_eyebrow", lang),
        "/",
        Hero(
            eyebrow=t("home_eyebrow", lang),
            headline=(Span(t("home_headline_1", lang)), Span(t("home_headline_2", lang), cls="text-accent"), Span(t("home_headline_3", lang))),
            lede=t("home_lede", lang),
            ctas=[(t("home_cta_see", lang), "/platform", True), (t("nav_talk_to_us", lang), "/contact", False)],
            lang=lang,
        ),

        Section_(
            Eyebrow(t("home_precedent", lang)),
            Heading(2, t("home_precedent_heading", lang), cls="mt-4 max-w-3xl"),
            Div(
                *[Div(name, cls="text-ink-muted text-sm md:text-base font-medium border border-line rounded-full px-4 py-2") for name in logos_row],
                cls="mt-10 flex flex-wrap gap-3",
            ),
            cls="border-b border-line",
        ),

        Section_(
            Div(
                Eyebrow(t("home_capabilities", lang)),
                Heading(2, t("home_cap_heading", lang), cls="mt-4 max-w-4xl"),
                P(t("home_cap_body", lang), cls="mt-5 text-ink-muted text-lg max-w-3xl"),
                cls="mb-14",
            ),
            Div(
                *[Pillar(n, title, body) for n, title, body in pillars],
                cls="grid md:grid-cols-2 lg:grid-cols-4 gap-5",
            ),
        ),

        Section_(
            Div(
                Eyebrow(t("home_where", lang)),
                Heading(2, t("home_where_heading", lang), cls="mt-4 max-w-4xl"),
                cls="mb-14",
            ),
            Div(
                _sector_link(t("sector_defense_title", lang), t("sector_defense_body", lang), "/solutions/defense"),
                _sector_link(t("sector_health_title", lang), t("sector_health_body", lang), "/solutions/healthcare"),
                _sector_link(t("sector_public_title", lang), t("sector_public_body", lang), "/solutions/public"),
                _sector_link(t("sector_financial_title", lang), t("sector_financial_body", lang), "/solutions/financial"),
                cls="grid md:grid-cols-2 gap-5",
            ),
            cls="border-y border-line bg-bg-elevated/40",
        ),

        Section_(
            Div(
                Eyebrow(t("home_selected_work", lang)),
                Heading(2, t("home_selected_heading", lang), cls="mt-4 max-w-3xl"),
                cls="mb-14 flex flex-col md:flex-row md:items-end md:justify-between gap-4",
            ),
            Div(
                *[CaseStudyCard(c, compact=True, lang=lang) for c in home_cases],
                cls="grid md:grid-cols-3 gap-5",
            ),
            Div(
                Button_(t("home_all_cases", lang), href="/case-studies", primary=False),
                cls="mt-10",
            ),
        ),

        Section_(
            Div(
                Div(
                    Eyebrow(t("nav_signal", lang)),
                    Heading(2, t("home_signal_heading", lang), cls="mt-4 max-w-3xl"),
                    P(t("home_signal_body", lang),
                        cls="mt-5 text-ink-muted text-lg max-w-2xl leading-relaxed",
                    ),
                    Button_(t("home_open_signal", lang), href="/signal", primary=True, cls="mt-8"),
                    cls="md:w-2/5",
                ),
                Div(
                    Div(id="signal-teaser", cls="w-full h-[360px]"),
                    cls="md:w-3/5 p-3 rounded-2xl bg-bg-elevated border border-line",
                ),
                cls="flex flex-col md:flex-row gap-10 items-stretch",
            ),
            cls="border-y border-line",
        ),

        NewsSection(
            category="home",
            title=t("home_news_title", lang),
            subtitle=t("home_news_subtitle", lang),
            lang=lang,
        ),

        CTASection(lang=lang),

        # Load Plotly only when signal teaser present (home page only)
        lang=lang,
        body_extra=[
            Script(src="https://cdn.plot.ly/plotly-2.35.2.min.js"),
            Script(NotStr(f"window.PLOTLY_TEASER = {_teaser_json()};")),
            Script(src="/static/signal.js"),
            Script(src="/static/three-hero.js", type="module"),
        ],
    )


def _sector_link(title, body, href):
    return A(
        Div(
            Div(
                Span(title, cls="text-ink text-xl font-medium tracking-tight"),
                Span("→", cls="text-accent text-xl ml-auto"),
                cls="flex items-center mb-3",
            ),
            P(body, cls="text-ink-muted text-sm leading-relaxed"),
            cls="p-7 rounded-2xl border border-line bg-bg-elevated hover:border-accent/50 hover:bg-bg-raised transition-all",
        ),
        href=href,
        cls="block",
    )


def _teaser_json():
    import json
    from content import signal as s
    nhs, _ = s.nhs_charts()
    # Simplify layout for teaser
    nhs["layout"]["title"]["text"] = "NHS England waiting list · treemap by specialty"
    nhs["layout"]["margin"] = {"l": 0, "r": 0, "t": 30, "b": 0}
    return json.dumps(nhs)


# ---------- /platform ----------

@rt("/platform")
def platform(request: Request):
    lang = _lang(request)
    pillars = [
        ("01", t("pillar_doc_intel", lang), t("plat_pillar_doc_body", lang)),
        ("02", t("pillar_forecasting", lang), t("plat_pillar_forecast_body", lang)),
        ("03", t("pillar_geo", lang), t("plat_pillar_geo_body", lang)),
        ("04", t("pillar_agents", lang), t("plat_pillar_agents_body", lang)),
    ]

    commitments = [
        (t("commit_audit_title", lang), t("commit_audit_body", lang)),
        (t("commit_open_title", lang), t("commit_open_body", lang)),
        (t("commit_gdpr_title", lang), t("commit_gdpr_body", lang)),
        (t("commit_eval_title", lang), t("commit_eval_body", lang)),
    ]

    return page(
        t("platform_eyebrow", lang),
        "/platform",
        Section_(
            Eyebrow(t("platform_eyebrow", lang)),
            Heading(1, t("platform_headline", lang), cls="mt-5 max-w-5xl"),
            P(t("platform_lede", lang),
                cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow(t("home_capabilities", lang)),
                Heading(2, t("platform_cap_heading", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(*[_platform_row(n, title, body) for n, title, body in pillars], cls="divide-y divide-line border-y border-line"),
        ),
        Section_(
            Div(
                Eyebrow(t("platform_commit_eyebrow", lang)),
                Heading(2, t("platform_commit_heading", lang), cls="mt-4 max-w-4xl"),
                cls="mb-14",
            ),
            Div(
                *[Div(
                    Heading(3, title, cls="mb-2"),
                    P(body, cls="text-ink-muted text-sm leading-relaxed"),
                    cls="p-7 rounded-2xl bg-bg-elevated border border-line",
                ) for title, body in commitments],
                cls="grid md:grid-cols-2 gap-5",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        CTASection(lang=lang),
        lang=lang,
        body_extra=[Script(src="/static/three-hero.js", type="module")],
    )


def _platform_row(number, title, body):
    return Div(
        Div(
            Div(number, cls="font-mono text-xs tracking-widest text-accent"),
            cls="md:w-24 shrink-0",
        ),
        Div(
            Heading(3, title, cls="mb-3"),
            P(body, cls="text-ink-muted leading-relaxed"),
            cls="flex-1",
        ),
        cls="flex flex-col md:flex-row gap-6 py-10",
    )


# ---------- /solutions/* ----------

SOLUTIONS = {
    "defense": {
        "title_key": "sol_defense_title",
        "headline_key": "sol_defense_headline",
        "lede_key": "sol_defense_lede",
        "pillars": [
            ("sol_def_pillar1_title", "sol_def_pillar1_body"),
            ("sol_def_pillar2_title", "sol_def_pillar2_body"),
            ("sol_def_pillar3_title", "sol_def_pillar3_body"),
        ],
        "case_ids": ["nl-justice-dataplatform", "nordic-city-signal", "uk-traffic-od"],
        "register": ["sol_reg_operational_confidence", "sol_reg_audit_trail", "sol_reg_human_authority"],
        "news_cat": "defense",
    },
    "healthcare": {
        "title_key": "sol_health_title",
        "headline_key": "sol_health_headline",
        "lede_key": "sol_health_lede",
        "pillars": [
            ("sol_health_pillar1_title", "sol_health_pillar1_body"),
            ("sol_health_pillar2_title", "sol_health_pillar2_body"),
            ("sol_health_pillar3_title", "sol_health_pillar3_body"),
        ],
        "case_ids": ["nordic-health-rwd", "nordic-health-panel", "microsoft-isd"],
        "register": ["sol_reg_gdpr", "sol_reg_ai_act", "sol_reg_clinical_audit"],
        "news_cat": "healthcare",
    },
    "public": {
        "title_key": "sol_public_title",
        "headline_key": "sol_public_headline",
        "lede_key": "sol_public_lede",
        "pillars": [
            ("sol_pub_pillar1_title", "sol_pub_pillar1_body"),
            ("sol_pub_pillar2_title", "sol_pub_pillar2_body"),
            ("sol_pub_pillar3_title", "sol_pub_pillar3_body"),
        ],
        "case_ids": ["uk-traffic-od", "nordic-city-signal", "dk-data-quality"],
        "register": ["sol_reg_open_source", "sol_reg_reference", "sol_reg_interop"],
        "news_cat": "public",
    },
    "financial": {
        "title_key": "sol_financial_title",
        "headline_key": "sol_financial_headline",
        "lede_key": "sol_financial_lede",
        "pillars": [
            ("sol_fin_pillar1_title", "sol_fin_pillar1_body"),
            ("sol_fin_pillar2_title", "sol_fin_pillar2_body"),
            ("sol_fin_pillar3_title", "sol_fin_pillar3_body"),
        ],
        "case_ids": ["dbrs-rmbs", "arm-forecasting", "microsoft-isd"],
        "register": ["sol_reg_prod_ml", "sol_reg_regulatory", "sol_reg_enterprise"],
        "news_cat": "financial",
    },
}


def _solution_page(slug, request: Request):
    lang = _lang(request)
    s = SOLUTIONS[slug]
    cases = [c for c in ALL_CASES if c["id"] in s["case_ids"]]

    return page(
        t(s["title_key"], lang),
        f"/solutions/{slug}",
        Section_(
            Eyebrow(t(s["title_key"], lang)),
            Heading(1, t(s["headline_key"], lang), cls="mt-5 max-w-5xl"),
            P(t(s["lede_key"], lang), cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            Div(
                *[Pill(t(r, lang)) for r in s["register"]],
                cls="mt-10 flex flex-wrap gap-2",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow(t("sol_where_focus", lang)),
                Heading(2, t("sol_three_focal", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[Pillar(f"0{i+1}", t(title_key, lang), t(body_key, lang)) for i, (title_key, body_key) in enumerate(s["pillars"])],
                cls="grid md:grid-cols-3 gap-5",
            ),
        ),
        Section_(
            Div(
                Eyebrow(t("sol_in_practice", lang)),
                Heading(2, t("sol_looks_like", lang), cls="mt-4 max-w-3xl"),
                cls="mb-14",
            ),
            Div(
                *[CaseStudyCard(c, lang=lang) for c in cases],
                cls="grid md:grid-cols-3 gap-5",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        NewsSection(category=s["news_cat"], title=t(s["title_key"], lang), lang=lang),
        CTASection(lang=lang),
        lang=lang,
    )


@rt("/solutions/defense")
def sol_defense(request: Request):
    return _solution_page("defense", request)


@rt("/solutions/healthcare")
def sol_health(request: Request):
    return _solution_page("healthcare", request)


@rt("/solutions/public")
def sol_public(request: Request):
    return _solution_page("public", request)


@rt("/solutions/financial")
def sol_financial(request: Request):
    return _solution_page("financial", request)


# ---------- /case-studies ----------

@rt("/case-studies")
def case_studies(request: Request):
    lang = _lang(request)
    return page(
        t("nav_case_studies", lang),
        "/case-studies",
        Section_(
            Eyebrow(t("nav_case_studies", lang)),
            Heading(1, t("cases_headline", lang), cls="mt-5 max-w-4xl"),
            P(t("cases_lede", lang),
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow(t("cases_current_eyebrow", lang)),
                Heading(2, t("cases_current_heading", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[CaseStudyCard(c, lang=lang) for c in BID_DERIVED],
                cls="grid md:grid-cols-2 gap-5",
            ),
        ),
        Section_(
            Div(
                Eyebrow(t("cases_named_eyebrow", lang)),
                Heading(2, t("cases_named_heading", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[CaseStudyCard(c, lang=lang) for c in NAMED_PRECEDENTS],
                cls="grid md:grid-cols-3 gap-5",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        CTASection(lang=lang),
        lang=lang,
    )


# ---------- /signal ----------

@rt("/signal")
def signal(request: Request):
    lang = _lang(request)
    charts = signal_mod.all_charts()
    tabs = []
    panels = []
    for key, block in charts.items():
        sig_title = t(f"sig_{key}_title", lang)
        sig_eyebrow = t(f"sig_{key}_eyebrow", lang)
        sig_summary = t(f"sig_{key}_summary", lang)
        tabs.append(
            Button(
                sig_title,
                type="button",
                cls="signal-tab",
                **{"data-signal-tab": key},
            )
        )
        panels.append(
            Div(
                Div(
                    Eyebrow(sig_eyebrow),
                    Heading(2, sig_title, cls="mt-4"),
                    P(sig_summary, cls="mt-5 text-ink-muted text-lg max-w-3xl leading-relaxed"),
                    cls="mb-10",
                ),
                Div(
                    Div(
                        Div(id=f"chart-{key}-primary", cls="w-full"),
                        cls="chart-frame md:col-span-2",
                    ),
                    Div(
                        Div(id=f"chart-{key}-secondary", cls="w-full"),
                        cls="chart-frame",
                    ),
                    cls="grid md:grid-cols-3 gap-5",
                ),
                Div(
                    Span(t("signal_source", lang), cls="text-ink-dim text-xs"),
                    A(block["source"]["label"], href=block["source"]["url"], target="_blank", cls="text-accent text-xs hover:underline"),
                    cls="mt-4",
                ),
                cls="hidden",
                **{"data-signal-panel": key},
            )
        )

    return page(
        "Signal",
        "/signal",
        Section_(
            Eyebrow(t("nav_signal", lang)),
            Heading(1, t("signal_headline", lang), cls="mt-5 max-w-5xl"),
            P(t("signal_lede", lang),
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(*tabs, cls="flex flex-wrap gap-3 mb-10"),
            Div(*panels),
            cls="border-t border-line",
        ),
        CTASection(
            headline=t("signal_cta_headline", lang),
            body=t("signal_cta_body", lang),
            lang=lang,
        ),
        lang=lang,
        body_extra=[
            Script(src="https://cdn.plot.ly/plotly-2.35.2.min.js"),
            Script(NotStr(f"window.PLOTLY_DATA = {signal_mod.as_json()};")),
            Script(src="/static/signal.js"),
        ],
    )


# ---------- /open-source ----------

@rt("/research")
def research_redirect():
    return RedirectResponse("/open-source", status_code=301)

@rt("/open-source")
def open_source(request: Request):
    lang = _lang(request)
    return page(
        "Open Source",
        "/open-source",
        Section_(
            Eyebrow(t("research_eyebrow", lang)),
            Heading(1, t("research_headline", lang), cls="mt-5 max-w-4xl"),
            P(t("research_lede", lang),
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            P(
                t("opensource_ec_note", lang) + " ",
                A(t("opensource_ec_link", lang) + " →",
                  href="https://digital-strategy.ec.europa.eu/en/policies/open-source-strategy",
                  target="_blank", cls="text-accent hover:underline"),
                cls="mt-6 text-ink-muted max-w-3xl leading-relaxed",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow(t("os_resilience_eyebrow", lang)),
                Heading(2, t("os_resilience_heading", lang), cls="mt-4 max-w-4xl"),
                P(t("os_resilience_body1", lang),
                  cls="mt-8 text-ink-muted text-lg max-w-3xl leading-relaxed mb-6"),
                P(t("os_resilience_body2", lang),
                  cls="text-ink-muted text-lg max-w-3xl leading-relaxed"),
                cls="max-w-4xl",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        Section_(
            Div(
                Eyebrow("Open-source app suite"),
                Heading(2, "Open Source Enterprise", cls="mt-4 max-w-3xl"),
                P(
                    "A complete suite of open-source business apps — CRM, helpdesk, ERP, HR, "
                    "mail, analytics and more — each with a built-in AI assistant. Free to use, "
                    "self-hostable, and yours to extend.",
                    cls="mt-6 text-ink-muted max-w-3xl leading-relaxed",
                ),
                cls="mb-14",
            ),
            *[
                Div(
                    Div(
                        Span(grp["category"], cls="text-ink font-medium"),
                        Span(grp["blurb"], cls="ml-3 text-ink-muted text-sm"),
                        cls="flex items-baseline mb-5 pb-3 border-b border-line",
                    ),
                    Div(
                        *[
                            A(
                                Div(
                                    Div(
                                        Span(app["name"], cls="font-semibold text-ink"),
                                        Span(
                                            app["feature"],
                                            cls="ml-auto text-[10px] font-mono tracking-widest px-2 py-0.5 rounded-full border border-accent text-accent",
                                        ),
                                        cls="flex items-center mb-3",
                                    ),
                                    P(app["tagline"], cls="text-ink-muted text-sm leading-relaxed mb-4"),
                                    Div(
                                        Span("Open source · MIT", cls="text-[11px] text-ink-muted"),
                                        Span("View →", cls="ml-auto text-accent text-sm"),
                                        cls="flex items-center",
                                    ),
                                    cls="p-6 rounded-2xl bg-bg-elevated border border-line hover:border-accent/50 transition-colors h-full",
                                ),
                                href=app["url"],
                                target="_blank",
                                cls="block",
                            )
                            for app in grp["apps"]
                        ],
                        cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mb-12",
                    ),
                )
                for grp in APP_SUITE
            ],
            cls="border-b border-line",
        ),
        Section_(
            Div(
                Eyebrow(t("research_repos_eyebrow", lang)),
                Heading(2, t("research_repos_heading", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[
                    A(
                        Div(
                            Div(
                                Span(r["name"], cls="font-mono text-ink text-sm"),
                                Span(r["relevance"], cls=f"ml-auto text-[10px] font-mono tracking-widest px-2 py-0.5 rounded-full border {'border-accent text-accent' if r['relevance']=='HIGH' else 'border-line text-ink-muted'}"),
                                cls="flex items-center mb-4",
                            ),
                            P(r["tagline"], cls="text-ink-muted text-sm leading-relaxed mb-4"),
                            Div(*[Pill(tag) for tag in r["tags"]], cls="flex flex-wrap gap-2"),
                            cls="p-6 rounded-2xl bg-bg-elevated border border-line hover:border-accent/50 transition-colors h-full",
                        ),
                        href=r["url"],
                        target="_blank",
                        cls="block",
                    )
                    for r in REPOS
                ],
                cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
        ),
        Section_(
            Div(
                Eyebrow(t("research_platforms_eyebrow", lang)),
                Heading(2, t("research_platforms_heading", lang), cls="mt-4 max-w-3xl"),
                cls="mb-14",
            ),
            Div(
                *[
                    A(
                        Div(
                            Heading(3, r["name"], cls="mb-3"),
                            P(r["tagline"], cls="text-ink-muted text-sm leading-relaxed mb-5"),
                            Div(
                                Span(t("research_visit", lang) + " ", cls="text-accent text-sm"),
                                Span("→", cls="text-accent text-sm"),
                            ),
                            cls="p-6 rounded-2xl bg-bg-elevated border border-line hover:border-accent/50 transition-colors h-full",
                        ),
                        href=r["url"],
                        target="_blank",
                        cls="block",
                    )
                    for r in EXTERNAL_RESEARCH
                ],
                cls="grid md:grid-cols-2 gap-5",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        CTASection(lang=lang),
        lang=lang,
    )


# ---------- /team ----------

@rt("/team")
def team(request: Request):
    lang = _lang(request)
    return page(
        "Team",
        "/team",
        Section_(
            Eyebrow(t("nav_team", lang)),
            Heading(1, t("team_headline", lang), cls="mt-5 max-w-4xl"),
            P(t("team_lede", lang),
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                *[_member_card(m, lang=lang) for m in TEAM],
                cls="grid md:grid-cols-2 gap-5",
            ),
        ),
        CTASection(headline=t("team_join_headline", lang), body=t("team_join_body", lang), cta_label=t("team_write", lang), lang=lang),
        lang=lang,
    )


def _member_card(m, *, lang="en"):
    ikey = m["initials"].lower()
    return Article(
        Div(
            Div(m["initials"], cls="w-14 h-14 rounded-full bg-bg-raised border border-line flex items-center justify-center text-ink font-mono text-sm"),
            Div(
                Heading(3, m["name"], cls="mb-1"),
                P(t(f"team_{ikey}_role", lang), cls="text-accent text-sm font-mono"),
            ),
            cls="flex items-center gap-4 mb-5",
        ),
        P(t(f"team_{ikey}_bio", lang), cls="text-ink-muted leading-relaxed mb-6"),
        A(
            Span("LinkedIn", cls="text-sm"),
            Span("→", cls="text-sm"),
            href=m["linkedin"],
            target="_blank",
            cls="inline-flex items-center gap-2 text-ink hover:text-accent transition-colors",
        ),
        cls="p-8 rounded-2xl bg-bg-elevated border border-line",
    )


# ---------- /thesis ----------

@rt("/thesis")
def thesis(request: Request):
    lang = _lang(request)
    proposals = [
        (t("thesis_p1_title", lang), t("thesis_p1_body", lang)),
        (t("thesis_p2_title", lang), t("thesis_p2_body", lang)),
        (t("thesis_p3_title", lang), t("thesis_p3_body", lang)),
        (t("thesis_p4_title", lang), t("thesis_p4_body", lang)),
        (t("thesis_p5_title", lang), t("thesis_p5_body", lang)),
        (t("thesis_p6_title", lang), t("thesis_p6_body", lang)),
    ]

    return page(
        t("thesis_eyebrow", lang),
        "/thesis",
        Section_(
            Eyebrow(t("thesis_eyebrow", lang)),
            Heading(1, t("thesis_headline", lang), cls="mt-5 max-w-5xl"),
            P(t("thesis_lede", lang), cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            Div(
                Pill(t("thesis_pill_sovereignty", lang)),
                Pill(t("thesis_pill_opensource", lang)),
                Pill(t("thesis_pill_policy", lang)),
                cls="mt-8 flex flex-wrap gap-2",
            ),
            cls="pt-24",
        ),
        Section_(
            Div(
                Eyebrow(t("thesis_proposals_eyebrow", lang)),
                Heading(2, t("thesis_proposals_heading", lang), cls="mt-4"),
                cls="mb-14",
            ),
            Div(
                *[Div(
                    Div(
                        Span(f"0{i+1}", cls="font-mono text-xs tracking-widest text-accent"),
                        cls="mb-4",
                    ),
                    Heading(3, title, cls="mb-3"),
                    P(body, cls="text-ink-muted text-sm leading-relaxed"),
                    cls="p-7 rounded-2xl bg-bg-elevated border border-line",
                ) for i, (title, body) in enumerate(proposals)],
                cls="grid md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
        ),
        Section_(
            Div(
                Eyebrow(t("resilience_eyebrow", lang)),
                Heading(2, t("resilience_heading", lang), cls="mt-4 max-w-4xl"),
                P(t("resilience_lede", lang),
                  cls="mt-8 text-ink-muted text-lg max-w-3xl leading-relaxed"),
                cls="mb-12",
            ),
            Div(
                *[Div(
                    Heading(3, title, cls="mb-3"),
                    P(body, cls="text-ink-muted text-sm leading-relaxed"),
                    cls="p-7 rounded-2xl bg-bg-elevated border border-line",
                ) for title, body in [
                    (t("resilience_c1_title", lang), t("resilience_c1_body", lang)),
                    (t("resilience_c2_title", lang), t("resilience_c2_body", lang)),
                    (t("resilience_c3_title", lang), t("resilience_c3_body", lang)),
                ]],
                cls="grid md:grid-cols-3 gap-5",
            ),
            cls="border-t border-line",
        ),
        Section_(
            Div(
                Eyebrow(t("thesis_why_eyebrow", lang)),
                Heading(2, t("thesis_why_heading", lang), cls="mt-4 max-w-4xl"),
                cls="mb-10",
            ),
            P(t("thesis_why_body1", lang), cls="text-ink-muted text-lg max-w-3xl leading-relaxed mb-8"),
            P(t("thesis_why_body2", lang), cls="text-ink-muted text-lg max-w-3xl leading-relaxed mb-10"),
            Div(
                Button_(t("thesis_read_more", lang), href="https://digital-strategy.ec.europa.eu/en/policies/open-source-strategy", primary=True),
                Button_(t("thesis_see_research", lang), href="/open-source", primary=False),
                cls="flex items-center gap-3 flex-wrap",
            ),
            cls="border-t border-line bg-bg-elevated/40",
        ),
        CTASection(
            headline=t("thesis_cta_headline", lang),
            body=t("thesis_cta_body", lang),
            lang=lang,
        ),
        lang=lang,
    )


# ---------- /contact ----------

@rt("/contact")
def contact(request: Request):
    lang = _lang(request)
    return page(
        t("nav_contact", lang),
        "/contact",
        Section_(
            Eyebrow(t("nav_contact", lang)),
            Heading(1, t("contact_headline", lang), cls="mt-5 max-w-4xl"),
            P(t("contact_lede", lang),
              cls="mt-8 text-xl text-ink-muted max-w-3xl leading-relaxed"),
            cls="pt-24",
        ),
        Section_(
            Div(
                Div(
                    Eyebrow(t("contact_write_eyebrow", lang)),
                    Heading(2, CONTACT_EMAIL, cls="mt-4 break-all"),
                    P(t("contact_write_body", lang),
                      cls="mt-5 text-ink-muted leading-relaxed"),
                    Div(
                        Button_(t("contact_email_btn", lang) + " " + CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}", primary=True),
                        cls="mt-8",
                    ),
                    cls="p-10 rounded-2xl bg-bg-elevated border border-line",
                ),
                Div(
                    Div(
                        H3(t("contact_reg_office", lang), cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Predictive Labs Ltd", cls="text-ink"),
                        P("155 Minories Street, Suite 275", cls="text-ink-muted"),
                        P("London, EC3N 1AD", cls="text-ink-muted"),
                        P("United Kingdom", cls="text-ink-muted"),
                        P("Company no. 14857334", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3(t("contact_lt_entity", lang), cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Predictive Labs, UAB", cls="text-ink"),
                        P("Medeinos g. 35-70", cls="text-ink-muted"),
                        P("Vilnius, LT-06137", cls="text-ink-muted"),
                        P("Lithuania", cls="text-ink-muted"),
                        P("Reg. code 307863496", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3(t("contact_ee_entity", lang), cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Predictive Labs OÜ", cls="text-ink"),
                        P("Karsti 3", cls="text-ink-muted"),
                        P("Tallinn, 11625", cls="text-ink-muted"),
                        P("Estonia", cls="text-ink-muted"),
                        P("Registry code 12061679", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3(t("contact_ee_entity_2", lang), cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Manmouna OÜ", cls="text-ink"),
                        P("Teelise tn 10, Nõmme linnaosa", cls="text-ink-muted"),
                        P("10916 Tallinn, Harju maakond", cls="text-ink-muted"),
                        P("Estonia", cls="text-ink-muted"),
                        P("Registry code 16289310", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3("Canada", cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Predictive Labs Inc.", cls="text-ink"),
                        P("155 East Beaver Creek Road, Suite 24-147", cls="text-ink-muted"),
                        P("Richmond Hill, Ontario, L4B 2N1", cls="text-ink-muted"),
                        P("Canada", cls="text-ink-muted"),
                        P("OCN 1001679945", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3("United States", cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        P("Predictive Labs LLC", cls="text-ink"),
                        P("1331 Grand Street, Suite 607", cls="text-ink-muted"),
                        P("Hoboken, NJ 07030", cls="text-ink-muted"),
                        P("United States", cls="text-ink-muted"),
                        P("ID 2025-001721250", cls="text-ink-dim text-sm mt-3 font-mono"),
                        cls="mb-10",
                    ),
                    Div(
                        H3(t("contact_channels", lang), cls="text-sm font-mono tracking-widest uppercase text-ink-muted mb-3"),
                        A("GitHub", href=GITHUB_URL, target="_blank", cls="block text-ink hover:text-accent mb-2"),
                        A("LinkedIn", href=LINKEDIN_URL, target="_blank", cls="block text-ink hover:text-accent mb-2"),
                    ),
                    cls="p-10 rounded-2xl bg-bg-elevated border border-line",
                ),
                cls="grid md:grid-cols-2 gap-5",
            ),
        ),
        lang=lang,
    )


if __name__ == "__main__":
    serve()
