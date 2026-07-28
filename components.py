"""Shared layout and components for FastSME."""

from datetime import datetime
from fasthtml.common import (
    Html, Head, Body, Meta, Title, Link, Script, Style, NotStr,
    Nav, Main, Footer, Section, Article, Div, Span, A, H1, H2, H3, H4,
    P, Ul, Li, Button, Strong,
)

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
    ("Open source", "/open-source"),
    ("Thesis", "/thesis"),
    ("Team", "/team"),
]


def Button_(label, href, primary=True):
    cls = (
        "inline-flex items-center gap-2 rounded-full px-5 py-3 text-sm font-semibold transition "
        + ("bg-forest text-white hover:bg-leaf" if primary else "border border-forest/20 text-forest hover:border-leaf hover:text-leaf")
    )
    return A(label, Span("↗"), href=href, cls=cls)


def Eyebrow(text):
    return Span(text, cls="text-xs font-semibold uppercase tracking-[.18em] text-leaf")


def Section_(*children, cls=""):
    return Section(Div(*children, cls="mx-auto max-w-7xl px-5 md:px-8"), cls=f"py-16 md:py-24 {cls}")


def Heading(text, level=2, cls=""):
    tag = {1: H1, 2: H2, 3: H3}[level]
    sizes = {1: "text-4xl sm:text-6xl lg:text-7xl", 2: "text-3xl md:text-5xl", 3: "text-xl md:text-2xl"}
    return tag(text, cls=f"font-display font-semibold tracking-[-.04em] leading-[1.05] text-forest {sizes[level]} {cls}")


def ProductCard(product):
    return Article(
        Div(
            Span(product["label"], cls="rounded-full bg-mint px-3 py-1 text-xs font-semibold text-forest"),
            Span("Open source", cls="text-xs text-muted"),
            cls="flex items-center justify-between gap-3",
        ),
        H3(product["name"], cls="mt-6 font-display text-2xl font-semibold tracking-tight text-forest"),
        P(product["description"], cls="mt-3 text-sm leading-6 text-muted"),
        A("View repository →", href=product["url"], target="_blank", rel="noopener", cls="mt-6 inline-block text-sm font-semibold text-leaf hover:text-forest"),
        cls="group rounded-3xl border border-line bg-paper p-6 shadow-[0_10px_35px_rgba(18,61,42,.05)] transition hover:-translate-y-1 hover:border-leaf/50",
    )


def Navbar(current="/"):
    links = [
        Li(A(label, href=href, cls=f"text-sm font-medium transition hover:text-leaf {'text-leaf' if current == href else 'text-forest'}"))
        for label, href in NAV
    ]
    mobile = [
        Li(A(label, href=href, cls="block py-2 text-lg font-medium text-forest hover:text-leaf"))
        for label, href in NAV
    ]
    return Nav(
        Div(
            A(
                Span("F", cls="flex h-8 w-8 items-center justify-center rounded-xl bg-leaf text-sm font-bold text-white"),
                Span("FastSME", cls="font-display text-lg font-bold tracking-tight text-forest"),
                href="/", cls="flex items-center gap-2",
            ),
            Ul(*links, cls="hidden items-center gap-7 lg:flex"),
            Div(
                A("Talk to us", href="/contact", cls="hidden rounded-full bg-forest px-4 py-2 text-sm font-semibold text-white hover:bg-leaf sm:block"),
                Button("☰", type="button", aria_label="Toggle navigation", onclick="document.getElementById('mobile-nav').classList.toggle('hidden')", cls="rounded-lg border border-line bg-white px-3 py-2 text-forest lg:hidden"),
                cls="flex items-center gap-3",
            ),
            cls="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 md:px-8",
        ),
        Div(Ul(*mobile, cls="space-y-1 px-5 py-5"), id="mobile-nav", cls="hidden border-t border-line bg-white lg:hidden"),
        cls="sticky top-0 z-50 border-b border-line bg-canvas/90 backdrop-blur",
    )


def Footer_():
    return Footer(
        Div(
            Div(
                Div(
                    H3("FastSME", cls="font-display text-2xl font-semibold text-white"),
                    P("Open enterprise software for ambitious small businesses everywhere.", cls="mt-3 max-w-sm text-sm leading-6 text-white/65"),
                ),
                Div(
                    H4("Explore", cls="text-xs font-semibold uppercase tracking-widest text-lime"),
                    *[A(label, href=href, cls="mt-3 block text-sm text-white/70 hover:text-white") for label, href in NAV],
                ),
                Div(
                    H4("Contact", cls="text-xs font-semibold uppercase tracking-widest text-lime"),
                    A(CONTACT_EMAIL, href=f"mailto:{CONTACT_EMAIL}", cls="mt-3 block text-sm text-white hover:text-lime"),
                    A("GitHub", href=GITHUB_URL, target="_blank", cls="mt-3 block text-sm text-white/70 hover:text-white"),
                ),
                cls="grid gap-10 md:grid-cols-[2fr_1fr_1fr]",
            ),
            Div(
                P(
                    Strong("Exroad Fintech Ltd, trading as FastSME"), NotStr("<br>"),
                    "Company number 11914994", NotStr("<br>"),
                    "155 Minories Street, Flat 275", NotStr("<br>"),
                    "London, United Kingdom, EC3N 1AD",
                    cls="text-xs leading-5 text-white/55",
                ),
                P(f"© {datetime.now().year} Exroad Fintech Ltd.", cls="text-xs text-white/45"),
                cls="mt-12 flex flex-col justify-between gap-6 border-t border-white/10 pt-8 md:flex-row md:items-end",
            ),
            cls="mx-auto max-w-7xl px-5 md:px-8",
        ),
        cls="bg-night py-14",
    )


def page(title, current, *content, description=None):
    description = description or SITE_TAGLINE
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
        ),
        Body(Navbar(current), Main(*content), Footer_(), cls="bg-canvas font-sans text-forest antialiased"),
        lang="en",
    )
