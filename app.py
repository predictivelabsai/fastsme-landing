"""FastSME — open enterprise software for SMEs and SMBs globally."""

import os
import json
import secrets
from urllib.parse import unquote, urlencode, urlsplit
from urllib.request import Request as UrlRequest, urlopen
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fasthtml.common import fast_app, serve, Div, Span, A, P, Section, Article, H3, Strong, NotStr

from components import page, Section_, Heading, Eyebrow, Button_, ProductCard, PartnerCard, CONTACT_EMAIL
from content.products import GROUPS, PRODUCTS, FEATURED
from content.clients import CLIENTS
from content.partners import PARTNERS
from content.team import TEAM, ADVISORY
from utils.i18n import LANGUAGES, get_lang, set_lang, t

app, rt = fast_app(static_path=".", secret_key=os.getenv("FASTSME_SESSION_SECRET", "fastsme-change-me"))


def _google_callback_uri(request):
    configured = os.getenv("GOOGLE_REDIRECT_URI")
    if configured:
        return configured
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    return f"{proto}://{host}/auth/google/callback"


@rt("/auth/google")
def google_start(sess, request):
    client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    if not client_id:
        return RedirectResponse("/?auth=not-configured", status_code=303)
    state = secrets.token_urlsafe(32)
    sess["google_oauth_state"] = state
    query = urlencode({"client_id": client_id, "redirect_uri": _google_callback_uri(request),
                       "response_type": "code", "scope": "openid email profile",
                       "state": state, "prompt": "select_account"})
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{query}", status_code=303)


@rt("/auth/google/callback")
def google_callback(sess, request, code: str = "", state: str = "", error: str = ""):
    if error or not code or state != sess.pop("google_oauth_state", None):
        return RedirectResponse("/?auth=failed", status_code=303)
    data = urlencode({"code": code, "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                      "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                      "redirect_uri": _google_callback_uri(request),
                      "grant_type": "authorization_code"}).encode()
    try:
        token = json.loads(urlopen(UrlRequest("https://oauth2.googleapis.com/token", data=data),
                                   timeout=20).read())
        info_req = UrlRequest("https://openidconnect.googleapis.com/v1/userinfo",
                              headers={"Authorization": f"Bearer {token['access_token']}"})
        info = json.loads(urlopen(info_req, timeout=20).read())
    except Exception:
        return RedirectResponse("/?auth=failed", status_code=303)
    if not info.get("email") or info.get("email_verified") is False:
        return RedirectResponse("/?auth=failed", status_code=303)
    sess["user_email"] = info["email"].strip().lower()
    return RedirectResponse("/products", status_code=303)


class CanonicalHostMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "").split(":")[0].lower()
        if host in {"www.fastsme.com", "fastsme.org", "www.fastsme.org"}:
            return RedirectResponse(f"https://fastsme.com{request.url.path}" + (f"?{request.url.query}" if request.url.query else ""), status_code=301)
        return await call_next(request)


app.add_middleware(CanonicalHostMiddleware)


def _safe_return_path(value):
    """Allow route preservation without permitting an external redirect."""
    value = value or "/"
    parsed = urlsplit(value)
    decoded = unquote(parsed.path)
    if (parsed.scheme or parsed.netloc or not decoded.startswith("/") or
            decoded.startswith("//") or "\\" in decoded or
            any(ord(character) < 32 for character in unquote(value))):
        return "/"
    return parsed.path + (f"?{parsed.query}" if parsed.query else "")


@rt("/set-lang/{code}")
def set_language(code: str, sess, next: str = "/"):
    if code in LANGUAGES:
        set_lang(sess, code)
    return RedirectResponse(_safe_return_path(next), status_code=303)


def _intro(eyebrow, title, body):
    return Section_(
        Eyebrow(eyebrow),
        Heading(title, 1, "mt-5 max-w-5xl"),
        P(body, cls="mt-7 max-w-3xl text-lg leading-8 text-muted md:text-xl"),
        cls="pt-20 md:pt-28",
    )


@rt("/")
def home(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    featured = [p for p in PRODUCTS if p["name"] in FEATURED]
    return page(
        "Open enterprise software for SMEs",
        "/",
        Section(
            Div(
                Div(
                    Eyebrow(T("Open source · affordable · globally useful")),
                    Heading(T("Big-company capability. Small-business economics."), 1, "mt-6 max-w-5xl"),
                    P(T("FastSME brings the software capabilities of large enterprises to SMEs and SMBs worldwide — as practical open-source products that are affordable to adopt, own and extend."), cls="mt-7 max-w-3xl text-lg leading-8 text-muted md:text-xl"),
                    Div(Button_("Explore 23 open-source products", "/products", lang=lang), Button_("Talk to the team", "/contact", False, lang), cls="mt-9 flex flex-wrap gap-3"),
                    cls="relative z-10",
                ),
                Div(
                    Span("OPEN", cls="absolute right-4 top-8 font-display text-[22vw] font-bold leading-none text-leaf/[.06]"),
                    cls="pointer-events-none absolute inset-0 overflow-hidden",
                ),
                cls="relative mx-auto flex min-h-[76vh] max-w-7xl items-center px-5 py-20 md:px-8",
            ),
            cls="border-b border-line bg-[radial-gradient(circle_at_80%_25%,#DDF5E5_0,transparent_38%)]",
        ),
        Section_(
            Div(
                Eyebrow(T("One connected portfolio")),
                Heading(T("Start with the problem you need to solve."), 2, "mt-4 max-w-3xl"),
                P(T("Use one product, combine several, or adapt the source to the way your business already works."), cls="mt-5 max-w-2xl leading-7 text-muted"),
                cls="mb-12",
            ),
            Div(*[ProductCard(p, lang) for p in featured], cls="grid gap-5 md:grid-cols-2 lg:grid-cols-3"),
            Div(Button_("See the complete portfolio", "/products", False, lang), cls="mt-10"),
        ),
        Section_(
            Div(
                Div(Eyebrow(T("Why FastSME")), Heading(T("Enterprise patterns without enterprise lock-in."), 2, "mt-4 max-w-3xl")),
                Div(
                    *[
                        Article(Span(f"0{i}", cls="text-xs font-bold text-leaf"), H3(T(title), cls="mt-4 font-display text-xl font-semibold"), P(T(body), cls="mt-3 text-sm leading-6 text-muted"))
                        for i, (title, body) in enumerate([
                            ("Open by default", "Inspect the code, self-host it and keep control of your data and roadmap."),
                            ("Designed to connect", "A consistent Python-first stack makes the suite easier to understand and integrate."),
                            ("AI where it helps", "Grounded assistants support real workflows instead of adding a decorative chatbot."),
                            ("Affordable ownership", "Avoid per-seat economics that punish growing teams."),
                        ], 1)
                    ],
                    cls="grid gap-8 sm:grid-cols-2",
                ),
                cls="grid gap-14 lg:grid-cols-2",
            ),
            cls="border-y border-line bg-mint/45",
        ),
        Section_(
            Eyebrow(T("Proven in demanding environments")),
            Heading(T("Experience shaped with global organisations."), 2, "mt-4 max-w-4xl"),
            Div(*[Span(name, cls="rounded-full border border-line bg-white px-4 py-2 text-sm font-semibold text-forest") for name, _, _ in CLIENTS[:10]], cls="mt-9 flex flex-wrap gap-3"),
            Div(Button_("See client experience", "/clients", False, lang), cls="mt-9"),
        ),
        Section_(
            Eyebrow(T("Integration partners")),
            Heading(T("Specialists who help the open suite connect and scale."), 2, "mt-4 max-w-4xl"),
            P(T("FastSME works with identity, engineering and applied-AI partners who can support integrations and delivery."), cls="mt-5 max-w-3xl leading-7 text-muted"),
            Div(*[PartnerCard(partner, lang) for partner in PARTNERS], cls="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3"),
            Div(Button_("Meet our partners", "/partners", False, lang), cls="mt-10"),
            cls="border-y border-line bg-mint/35",
        ),
        Section_(
            Div(
                Div(Eyebrow(T("A better software bargain")), Heading(T("Your tools should compound your advantage — not your licence bill."), 2, "mt-4 max-w-4xl"), P(T("FastSME is building a durable open-source layer for the businesses that create most of the world's jobs, but are too often priced out of the best technology."), cls="mt-6 max-w-3xl text-lg leading-8 text-muted")),
                Div(Button_("Read our thesis", "/thesis", lang=lang), Button_(CONTACT_EMAIL, f"mailto:{CONTACT_EMAIL}", False, lang), cls="mt-9 flex flex-wrap gap-3"),
                cls="rounded-[2rem] bg-forest p-8 text-white md:p-14 [&_h2]:!text-white [&_p]:!text-white/70",
            ),
        ),
        lang=lang,
    )


@rt("/products")
def products(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    sections = []
    for group in GROUPS:
        group_products = [p for p in PRODUCTS if p["category"] == group["name"]]
        sections.append(Section_(
            Div(Eyebrow(T(group["name"])), Heading(T(group["name"]), 2, "mt-3"), P(T(group["description"]), cls="mt-4 text-muted"), cls="mb-10"),
            Div(*[ProductCard(p, lang) for p in group_products], cls="grid gap-5 md:grid-cols-2 lg:grid-cols-3"),
            cls="border-t border-line first:border-0",
        ))
    return page("Products", "/products", _intro(T("23 open-source products · one open platform"), T("Tools for every stage of running a business."), T("From first customer to complex operations, FastSME gives smaller businesses a practical route to software normally reserved for large enterprises.")), *sections, lang=lang)


@rt("/clients")
def clients(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Clients", "/clients",
        _intro(T("Client experience"), T("Built through real enterprise delivery."), T("Our products are shaped by hands-on work across technology, finance, industry, healthcare, retail, energy and real estate.")),
        Section_(
            Div(*[
                Article(Span(T(sector), cls="text-xs font-semibold uppercase tracking-widest text-leaf"), H3(name, cls="mt-4 font-display text-2xl font-semibold"), P(T(work), cls="mt-3 text-sm leading-6 text-muted"), cls="rounded-3xl border border-line bg-white p-7")
                for name, sector, work in CLIENTS
            ], cls="grid gap-5 md:grid-cols-2 lg:grid-cols-3"),
            P(T("Selected client and professional experience of FastSME's owner and team. Descriptions are intentionally concise and exclude confidential details."), cls="mt-8 text-xs leading-5 text-muted"),
        ),
        lang=lang,
    )


@rt("/partners")
def partners(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Partners", "/partners",
        _intro(T("Integration partners"), T("Specialists who help FastSME connect and scale."), T("Our integration partners bring identity, software delivery, data engineering and applied-AI expertise to FastSME implementations.")),
        Section_(
            Div(*[PartnerCard(partner, lang) for partner in PARTNERS], cls="grid gap-5 md:grid-cols-2 lg:grid-cols-3"),
            P(T("Partner descriptions are based on each organisation's public profile. Follow the links for current services and capabilities."), cls="mt-8 text-xs leading-5 text-muted"),
        ),
        lang=lang,
    )


@rt("/open-source")
def open_source(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Open source", "/open-source",
        _intro(T("Built in the open"), T("Software you can inspect, run and improve."), T("Open source changes the economics of business software: you can understand what a system does, choose where it runs and build on it without waiting for a vendor.")),
        Section_(
            Div(*[
                Article(Span(str(i).zfill(2), cls="text-xs font-bold text-leaf"), Heading(T(title), 3, "mt-5"), P(T(body), cls="mt-4 leading-7 text-muted"), cls="rounded-3xl border border-line bg-white p-7")
                for i, (title, body) in enumerate([
                    ("Own the deployment", "Run FastSME products on your infrastructure, in your cloud or with a trusted operator."),
                    ("Keep your data portable", "Open code and conventional storage reduce dependence on one supplier's platform."),
                    ("Adapt the workflow", "Change the product around the way your company creates value — not the other way around."),
                    ("Share the progress", "Reusable improvements can benefit thousands of businesses facing the same operational problems."),
                ], 1)
            ], cls="grid gap-5 md:grid-cols-2"),
            Div(Button_("Browse all repositories", "https://github.com/predictivelabsai", lang=lang), Button_("Explore products", "/products", False, lang), cls="mt-10 flex flex-wrap gap-3"),
        ),
        lang=lang,
    )


@rt("/thesis")
def thesis(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Thesis", "/thesis",
        _intro(T("Our thesis"), T("The next productivity leap belongs to small business."), T("SMEs and SMBs create extraordinary value, but their software choices are often a compromise between limited tools and enterprise suites whose cost and complexity do not fit.")),
        Section_(
            Div(
                Div(Heading(T("Large enterprises already know what good operational software can do."), 2), P(T("Integrated data, automated workflows, governed access and decision support have become structural advantages. Smaller companies deserve the same leverage without copying enterprise bureaucracy."), cls="mt-6 text-lg leading-8 text-muted")),
                Div(*[
                    Article(Strong(T(title), cls="font-display text-lg text-forest"), P(T(body), cls="mt-2 text-sm leading-6 text-muted"))
                    for title, body in [
                        ("Open source lowers the floor.", "The core capability can be shared instead of rebuilt and relicensed for every company."),
                        ("A common stack lowers complexity.", "Consistent architecture makes products easier to deploy, integrate and maintain."),
                        ("Services remain local.", "Partners can customise, host and support software close to each business and market."),
                        ("AI changes the interface.", "Small teams can operate sophisticated systems through grounded, conversational assistance."),
                    ]
                ], cls="grid gap-6"),
                cls="grid gap-16 lg:grid-cols-2",
            ),
            cls="border-y border-line bg-mint/40",
        ),
        Section_(Heading(T("Our goal is simple: make excellent business software a shared global utility."), 2, "max-w-5xl"), Div(Button_("See what we are building", "/products", lang=lang), cls="mt-8")),
        lang=lang,
    )


def _person_card(person, lang="en"):
    links = [
        A(t("LinkedIn →", lang), href=person["linkedin"], target="_blank", rel="noopener",
          cls="text-sm font-semibold text-forest hover:text-leaf"),
    ]
    if person.get("website"):
        links.append(
            A(t("Website ↗", lang), href=person["website"], target="_blank", rel="noopener",
              cls="text-sm font-semibold text-forest/70 hover:text-leaf"),
        )
    return Article(
        Div(Span(person["initials"], cls="flex h-12 w-12 items-center justify-center rounded-2xl bg-mint text-sm font-bold text-forest"), Div(H3(person["name"], cls="font-display text-xl font-semibold"), P(t(person["role"], lang), cls="mt-1 text-xs font-semibold text-leaf")), cls="flex items-center gap-4"),
        P(t(person["bio"], lang), cls="mt-5 text-sm leading-6 text-muted"),
        Div(*links, cls="mt-5 flex flex-wrap gap-x-5 gap-y-2"),
        cls="rounded-3xl border border-line bg-white p-7",
    )


@rt("/team")
def team(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Team", "/team",
        _intro(T("Team"), T("Builders, operators and specialist advisers."), T("FastSME combines experience in enterprise delivery, open-source engineering, AI, fintech, healthcare and digital operations.")),
        Section_(Eyebrow(T("Core team")), Div(*[_person_card(p, lang) for p in TEAM], cls="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3")),
        Section_(Eyebrow(T("Advisory board")), Heading(T("Experience around the table."), 2, "mt-4"), Div(*[_person_card(p, lang) for p in ADVISORY], cls="mt-10 grid gap-5 md:grid-cols-2"), cls="border-t border-line bg-mint/35"),
        lang=lang,
    )


@rt("/contact")
def contact(sess, request):
    lang = get_lang(sess, request)
    T = lambda text: t(text, lang)
    return page(
        "Contact", "/contact",
        _intro(T("Contact"), T("Tell us what your business needs to run better."), T("Whether you want to adopt an existing FastSME product, combine several tools or sponsor a missing capability, start with a direct conversation.")),
        Section_(
            Div(
                Div(Eyebrow(T("Write to us")), Heading(CONTACT_EMAIL, 2, "mt-4 break-all"), P(T("We welcome SMEs, implementation partners, open-source contributors and organisations that want to sponsor useful shared software."), cls="mt-5 max-w-xl leading-7 text-muted"), Div(Button_("Send an email", f"mailto:{CONTACT_EMAIL}", lang=lang), cls="mt-8")),
                Div(H3(T("Registered office"), cls="font-display text-xl font-semibold"), P(Strong("Exroad Fintech Ltd"), NotStr("<br>"), T("trading as FastSME"), NotStr("<br><br>"), T("Company number 11914994"), NotStr("<br><br>"), "155 Minories Street, Flat 275", NotStr("<br>"), T("London, United Kingdom"), NotStr("<br>"), "EC3N 1AD", cls="mt-5 text-sm leading-6 text-muted")),
                cls="grid gap-12 rounded-[2rem] border border-line bg-white p-8 md:grid-cols-[2fr_1fr] md:p-12",
            )
        ),
        lang=lang,
    )


@rt("/healthz")
def healthz():
    return JSONResponse({"status": "ok", "service": "fastsme"})


@rt("/robots.txt")
def robots():
    return PlainTextResponse("User-agent: *\nAllow: /\nSitemap: https://fastsme.com/sitemap.xml\n")


@rt("/sitemap.xml")
def sitemap():
    paths = ["", "/products", "/clients", "/partners", "/open-source", "/thesis", "/team", "/contact"]
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://fastsme.com{p}</loc></url>" for p in paths) + "</urlset>"
    return PlainTextResponse(xml, media_type="application/xml")


for old_path, new_path in {
    "/platform": "/products", "/case-studies": "/clients", "/research": "/open-source",
    "/signal": "/products", "/solutions/defense": "/products", "/solutions/healthcare": "/products",
    "/solutions/public": "/products", "/solutions/financial": "/products",
}.items():
    def _make_redirect(target):
        def _redirect():
            return RedirectResponse(target, status_code=301)
        return _redirect
    rt(old_path)(_make_redirect(new_path))


if __name__ == "__main__":
    serve(port=int(os.environ.get("PORT", "5001")))
