"""Shared layout and components for FastSME."""

from datetime import datetime
from urllib.parse import quote
from fasthtml.common import (
    Html, Head, Body, Meta, Title, Link, Script, Style, NotStr,
    Nav, Main, Footer, Section, Article, Div, Span, A, H1, H2, H3, H4,
    P, Ul, Li, Button, Strong, Img,
)
from utils.i18n import LANGUAGES, t

SITE_NAME = "FastSME"
SITE_TAGLINE = "Open enterprise software for ambitious small businesses."
CONTACT_EMAIL = "info@fastsme.com"
GITHUB_URL = "https://github.com/predictivelabsai"

TAILWIND_CONFIG = """
tailwind.config={theme:{extend:{colors:{
  canvas:'#F7FCF7',paper:'#FFFFFF',forest:'#123D2A',muted:'#587064',
  line:'#D8E9DC',leaf:'#36A269',mint:'#DDF5E5',lime:'#BDF27B',night:'#09281B'
},fontFamily:{sans:['Inter','system-ui','sans-serif'],display:['Manrope','Inter','sans-serif']}}}}
"""

NAV = [
    ("Products", "/products"),
    ("Clients", "/clients"),
    ("Partners", "/partners"),
    ("Open source", "/open-source"),
    ("Thesis", "/thesis"),
    ("Team", "/team"),
]


def Button_(label, href, primary=True, lang="en"):
    cls = (
        "inline-flex items-center gap-2 rounded-full px-5 py-3 text-sm font-semibold transition "
        + ("bg-forest text-white hover:bg-leaf" if primary else "border border-forest/20 text-forest hover:border-leaf hover:text-leaf")
    )
    return A(t(label, lang), Span("↗"), href=href, cls=cls)


def Eyebrow(text):
    return Span(text, cls="text-xs font-semibold uppercase tracking-[.18em] text-leaf")


def Section_(*children, cls="", **attrs):
    return Section(Div(*children, cls="mx-auto max-w-7xl px-5 md:px-8"), cls=f"py-16 md:py-24 {cls}", **attrs)


def Heading(text, level=2, cls=""):
    tag = {1: H1, 2: H2, 3: H3}[level]
    sizes = {1: "text-4xl sm:text-6xl lg:text-7xl", 2: "text-3xl md:text-5xl", 3: "text-xl md:text-2xl"}
    return tag(text, cls=f"font-display font-semibold tracking-[-.04em] leading-[1.05] text-forest {sizes[level]} {cls}")


def ProductCard(product, lang="en"):
    links = []
    if product.get("demo_url"):
        links.append(A(t("Open live demo →", lang), href=product["demo_url"], target="_blank",
                       rel="noopener", cls="text-sm font-semibold text-leaf hover:text-forest"))
    links.append(A(t("View on GitHub ↗", lang), href=product["url"], target="_blank", rel="noopener",
                   cls="text-sm font-semibold text-forest/70 hover:text-leaf"))
    search_text = " ".join((
        product["name"],
        t(product["label"], lang),
        t(product["description"], lang),
        t(product["category"], lang),
    )).lower()
    return Article(
        Div(
            Span(t(product["label"], lang), cls="rounded-full bg-mint px-3 py-1 text-xs font-semibold text-forest"),
            Span(t("Open source", lang), cls="text-xs text-muted"),
            cls="flex items-center justify-between gap-3",
        ),
        H3(product["name"], cls="mt-6 font-display text-2xl font-semibold tracking-tight text-forest"),
        P(t(product["description"], lang), cls="mt-3 text-sm leading-6 text-muted"),
        Div(*links, cls="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2"),
        cls="product-card group rounded-3xl border border-line bg-paper p-6 shadow-[0_10px_35px_rgba(18,61,42,.05)] transition hover:-translate-y-1 hover:border-leaf/50",
        data_category=product["category_id"],
        data_search=search_text,
    )


def PartnerCard(partner, lang="en"):
    return Article(
        Div(
            Img(
                src=partner["logo"],
                alt=f'{partner["name"]} logo',
                loading="lazy",
                cls="h-12 w-12 object-contain",
            ),
            Span(t("Integration Partner", lang), cls="rounded-full bg-mint px-3 py-1 text-xs font-semibold text-forest"),
            cls="flex items-center justify-between gap-4",
        ),
        H3(partner["name"], cls="mt-6 font-display text-2xl font-semibold tracking-tight text-forest"),
        P(t(partner["description"], lang), cls="mt-3 text-sm leading-6 text-muted"),
        A(
            t("Visit website ↗", lang),
            href=partner["url"],
            target="_blank",
            rel="noopener noreferrer",
            cls="mt-6 inline-flex text-sm font-semibold text-leaf hover:text-forest",
        ),
        cls="rounded-3xl border border-line bg-white p-7 shadow-[0_10px_35px_rgba(18,61,42,.05)] transition hover:-translate-y-1 hover:border-leaf/50",
    )


def _language_switcher(lang, current):
    current_language = LANGUAGES.get(lang, LANGUAGES["en"])
    return Div(
        Button(
            current_language["flag"],
            type="button",
            id="language-menu-button",
            aria_label=t("Choose language", lang),
            aria_haspopup="true",
            aria_expanded="false",
            onclick="toggleLanguageMenu(event)",
            cls="rounded-md border border-transparent bg-transparent px-1.5 py-1 text-base leading-none transition hover:border-line focus:outline-none focus:ring-2 focus:ring-leaf/40",
        ),
        Div(
            *[
                A(
                    Span(info["flag"], cls="text-base"),
                    Span(info["native"], cls="text-xs"),
                    href=f"/set-lang/{code}?next={quote(current, safe='/')}",
                    lang=code,
                    role="menuitem",
                    aria_current="true" if code == lang else None,
                    cls=(
                        "flex items-center gap-2 px-3 py-1.5 text-sm text-muted no-underline transition-colors "
                        "hover:bg-mint/50 hover:text-forest focus:bg-mint/50 focus:text-forest focus:outline-none"
                        + (" bg-mint/35 font-semibold text-forest" if code == lang else "")
                    ),
                )
                for code, info in LANGUAGES.items()
            ],
            id="language-menu",
            role="menu",
            cls="absolute right-0 top-full z-[60] mt-1 hidden min-w-[142px] flex-col rounded-lg border border-line bg-white py-1 shadow-xl",
        ),
        cls="relative",
    )


def Navbar(current="/", signed_in=False, lang="en"):
    links = [
        Li(A(t(label, lang), href=href, cls=f"text-sm font-medium transition hover:text-leaf {'text-leaf' if current == href else 'text-forest'}"))
        for label, href in NAV
    ]
    mobile = [
        Li(A(t(label, lang), href=href, cls="block py-2 text-lg font-medium text-forest hover:text-leaf"))
        for label, href in NAV
    ]
    return Nav(
        Div(
            A(
                Span("F", cls="flex h-8 w-8 items-center justify-center rounded-xl bg-leaf text-sm font-bold text-white"),
                Span("FastSME", cls="hidden font-display text-lg font-bold tracking-tight text-forest min-[370px]:inline"),
                href="/", cls="flex items-center gap-2",
            ),
            Ul(*links, cls="hidden items-center gap-7 lg:flex"),
            Div(
                _language_switcher(lang, current),
                A(t("Signed in" if signed_in else "Sign In", lang),
                  href="/products" if signed_in else "/auth/google",
                  cls="rounded-full border border-forest/20 px-3 py-2 text-xs font-semibold text-forest hover:border-leaf hover:text-leaf sm:px-4 sm:text-sm"),
                A(t("Talk to us", lang), href="/contact", cls="hidden rounded-full bg-forest px-4 py-2 text-sm font-semibold text-white hover:bg-leaf md:block"),
                Button("☰", type="button", aria_label=t("Toggle navigation", lang), onclick="document.getElementById('mobile-nav').classList.toggle('hidden')", cls="rounded-lg border border-line bg-white px-3 py-2 text-forest lg:hidden"),
                cls="flex items-center gap-2 sm:gap-3",
            ),
            cls="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 md:px-8",
        ),
        Div(Ul(*mobile, cls="space-y-1 px-5 py-5"), id="mobile-nav", cls="hidden border-t border-line bg-white lg:hidden"),
        cls="sticky top-0 z-50 border-b border-line bg-canvas/90 backdrop-blur",
    )


def Footer_(lang="en"):
    return Footer(
        Div(
            Div(
                Div(
                    H3("FastSME", cls="font-display text-2xl font-semibold text-white"),
                    P(t("Open enterprise software for ambitious small businesses everywhere.", lang), cls="mt-3 max-w-sm text-sm leading-6 text-white/65"),
                ),
                Div(
                    H4(t("Explore", lang), cls="text-xs font-semibold uppercase tracking-widest text-lime"),
                    *[A(t(label, lang), href=href, cls="mt-3 block text-sm text-white/70 hover:text-white") for label, href in NAV],
                ),
                Div(
                    H4(t("Contact", lang), cls="text-xs font-semibold uppercase tracking-widest text-lime"),
                    A(CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}", cls="mt-3 block text-sm text-white hover:text-lime"),
                    A("GitHub", href=GITHUB_URL, target="_blank", rel="noopener", cls="mt-3 block text-sm text-white/70 hover:text-white"),
                ),
                cls="grid gap-10 md:grid-cols-[2fr_1fr_1fr]",
            ),
            Div(
                P(
                    Strong(t("Powered by Predictive Labs Ltd", lang)), NotStr("<br><br>"),
                    "Predictive Labs Ltd", NotStr("<br>"),
                    "Company House Reg No: 14857334", NotStr("<br>"),
                    "155 Minories Street, Suite 275", NotStr("<br>"),
                    "London, EC3N 1AD, United Kingdom",
                    cls="text-xs leading-5 text-white/55",
                ),
                P(f"© {datetime.now().year} Predictive Labs Ltd.", cls="text-xs text-white/45"),
                cls="mt-12 flex flex-col justify-between gap-6 border-t border-white/10 pt-8 md:flex-row md:items-end",
            ),
            cls="mx-auto max-w-7xl px-5 md:px-8",
        ),
        cls="bg-night py-14",
    )


def page(title, current, *content, description=None, signed_in=False, lang="en"):
    title = t(title, lang)
    description = t(description or SITE_TAGLINE, lang)
    return Html(
        Head(
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="description", content=description),
            Meta(name="theme-color", content="#F7FCF7"),
            Link(rel="canonical", href=f"https://fastsme.com{current if current != '/' else ''}"),
            Meta(property="og:title", content=f"{title} · FastSME"),
            Meta(property="og:description", content=description),
            Meta(property="og:type", content="website"),
            Title(f"{title} · FastSME"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@500;600;700&display=swap"),
            Script(src="https://cdn.tailwindcss.com"),
            Script(NotStr(TAILWIND_CONFIG)),
            Link(rel="icon", type="image/svg+xml", href="/static/favicon.svg"),
            Link(rel="stylesheet", href="/static/site.css"),
            Script(NotStr("""
                function closeLanguageMenu() {
                    const menu = document.getElementById('language-menu');
                    const button = document.getElementById('language-menu-button');
                    if (menu) menu.classList.add('hidden');
                    if (button) button.setAttribute('aria-expanded', 'false');
                }
                function toggleLanguageMenu(event) {
                    event.stopPropagation();
                    const menu = document.getElementById('language-menu');
                    const button = document.getElementById('language-menu-button');
                    const opening = menu.classList.contains('hidden');
                    menu.classList.toggle('hidden');
                    button.setAttribute('aria-expanded', opening ? 'true' : 'false');
                    if (opening) menu.querySelector('a').focus();
                }
                let activeProductCategory = 'all';
                function filterProducts() {
                    const search = (document.getElementById('product-search')?.value || '').trim().toLowerCase();
                    let visible = 0;
                    document.querySelectorAll('.product-card').forEach(function(card) {
                        const categoryMatch = activeProductCategory === 'all' || card.dataset.category === activeProductCategory;
                        const searchMatch = !search || card.dataset.search.includes(search);
                        const show = categoryMatch && searchMatch;
                        card.hidden = !show;
                        if (show) visible += 1;
                    });
                    document.querySelectorAll('.product-group').forEach(function(group) {
                        group.hidden = !group.querySelector('.product-card:not([hidden])');
                    });
                    const count = document.getElementById('product-result-count');
                    if (count) count.textContent = visible;
                    const empty = document.getElementById('product-empty');
                    if (empty) empty.hidden = visible !== 0;
                }
                function setProductCategory(category, button) {
                    activeProductCategory = category;
                    document.querySelectorAll('.product-filter').forEach(function(item) {
                        const active = item === button;
                        item.setAttribute('aria-pressed', active ? 'true' : 'false');
                        item.classList.toggle('product-filter-active', active);
                    });
                    filterProducts();
                }
                document.addEventListener('click', closeLanguageMenu);
                document.addEventListener('keydown', function(event) {
                    if (event.key === 'Escape') {
                        closeLanguageMenu();
                        const button = document.getElementById('language-menu-button');
                        if (button) button.focus();
                    }
                });
            """)),
        ),
        Body(Navbar(current, signed_in, lang), Main(*content), Footer_(lang), cls="bg-canvas font-sans text-forest antialiased"),
        lang=lang,
    )
