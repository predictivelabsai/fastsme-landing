"""Browser smoke tests for the FastSME landing site."""

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    pytest.skip("playwright not installed", allow_module_level=True)

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "output" / "playwright"
OUTPUT.mkdir(parents=True, exist_ok=True)
PORT = 5011

ROUTES = [
    ("/", "home", "Big-company capability"),
    ("/products", "products", "Tools for every stage"),
    ("/clients", "clients", "real enterprise delivery"),
    ("/partners", "partners", "help FastSME connect and scale"),
    ("/open-source", "open-source", "inspect, run and improve"),
    ("/thesis", "thesis", "productivity leap"),
    ("/team", "team", "Builders, operators"),
    ("/contact", "contact", "business needs"),
]


def _wait(timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket() as sock:
            try:
                sock.connect(("127.0.0.1", PORT))
                return
            except OSError:
                time.sleep(.2)
    raise TimeoutError("FastSME test server did not start")


@pytest.fixture(scope="session")
def server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=ROOT,
    )
    try:
        _wait()
        yield f"http://127.0.0.1:{PORT}"
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.mark.parametrize("path,slug,expected", ROUTES)
def test_route(server, path, slug, expected):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(server + path, wait_until="networkidle")
        assert expected.lower() in page.locator("h1").first.inner_text().lower()
        assert page.get_by_text("Powered by Predictive Labs Ltd", exact=True).count() == 1
        page.screenshot(path=str(OUTPUT / f"{slug}.png"), full_page=True)
        browser.close()


def test_mobile_navigation(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(server, wait_until="networkidle")
        page.get_by_role("button", name="Toggle navigation").click()
        assert page.locator("#mobile-nav").is_visible()
        page.screenshot(path=str(OUTPUT / "home-mobile-nav.png"), full_page=True)
        browser.close()


def test_language_dropdown_preserves_route_and_session(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(server + "/products", wait_until="networkidle")
        trigger = page.locator("#language-menu-button")
        trigger.click()
        menu = page.locator("#language-menu")
        assert menu.is_visible()
        estonian = menu.get_by_role("menuitem", name="Eesti")
        assert estonian.get_attribute("href") == "/set-lang/et?next=/products"
        estonian.click()
        page.wait_for_url("**/products")
        assert page.locator("html").get_attribute("lang") == "et"
        assert "Tööriistad" in page.locator("h1").inner_text()
        page.goto(server + "/team", wait_until="networkidle")
        assert page.locator("html").get_attribute("lang") == "et"
        trigger = page.locator("#language-menu-button")
        trigger.click()
        page.keyboard.press("Escape")
        assert not page.locator("#language-menu").is_visible()
        assert trigger.get_attribute("aria-expanded") == "false"
        browser.close()


def test_every_supported_language_renders_translated_products(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for lang in ("en", "et", "de", "fr", "sv", "lv", "no", "da", "pl", "nl", "fi", "lt"):
            context = browser.new_context(locale="en-GB")
            page = context.new_page()
            page.goto(server + f"/set-lang/{lang}?next=/products", wait_until="networkidle")
            assert page.url.endswith("/products")
            assert page.locator("html").get_attribute("lang") == lang
            assert page.locator("#language-menu [role=menuitem]").count() == 12
            context.close()
        browser.close()


def test_language_return_path_rejects_external_redirects(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(server + "/set-lang/de?next=https://example.com", wait_until="networkidle")
        assert page.url == server + "/"
        assert page.locator("html").get_attribute("lang") == "de"
        page.goto(server + "/set-lang/fr?next=/%255cexample.com", wait_until="networkidle")
        assert page.url == server + "/"
        browser.close()


def test_language_and_sign_in_controls_fit_mobile_header(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 320, "height": 844})
        page.goto(server + "/set-lang/fr?next=/", wait_until="networkidle")
        language = page.locator("#language-menu-button")
        sign_in = page.get_by_role("link", name="Se connecter", exact=True)
        assert language.is_visible()
        assert sign_in.is_visible()
        for control in (language, sign_in):
            box = control.bounding_box()
            assert box and box["x"] >= 0 and box["x"] + box["width"] <= 320
        browser.close()


def test_partners_follow_clients_and_link_to_profiles(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(server + "/partners", wait_until="networkidle")
        nav_labels = page.locator("nav ul").first.locator("a").all_inner_texts()
        assert nav_labels[nav_labels.index("Clients") + 1] == "Partners"
        cards = page.locator("main article")
        assert cards.count() == 6
        assert cards.filter(has_text="SAASPASS").get_by_role("img", name="SAASPASS logo").count() == 1
        assert cards.filter(has_text="SAASPASS").get_by_role("link", name="Visit website").get_attribute("href") == "https://saaspass.com/"
        assert cards.filter(has_text="Consistente").get_by_role("link", name="Visit website").get_attribute("href") == "https://consistente.tech/"
        assert cards.filter(has_text="Manmouna Technologies").get_by_role("link", name="Visit website").get_attribute("href") == "https://manmouna.tech/"
        assert page.get_by_text("Integration Partner", exact=True).count() == 6
        browser.close()


def test_product_catalogue_starts_with_fastoffice(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(server + "/products", wait_until="networkidle")
        cards = page.locator("article")
        assert cards.first.locator("h3").inner_text() == "FastOffice"
        assert cards.first.get_by_role("link", name="Open live demo").get_attribute("href") == "https://fastoffice.org"
        fastcal = cards.filter(has_text="FastCal")
        assert fastcal.get_by_role("link", name="Open live demo").get_attribute("href") == "https://cal.fastsme.com"
        fastbooking = cards.filter(has_text="FastBooking")
        assert fastbooking.get_by_role("link", name="Open live demo").get_attribute("href") == "https://booking.fastsme.com"
        assert fastbooking.get_by_role("link", name="View on GitHub").get_attribute("href") == "https://github.com/predictivelabsai/FastBooking"
        fastaccounts = cards.filter(has_text="FastAccounts")
        assert fastaccounts.get_by_role("link", name="Open live demo").get_attribute("href") == "https://fastaccounts.org"
        assert fastaccounts.get_by_role("link", name="View on GitHub").get_attribute("href") == "https://github.com/predictivelabsai/FastAccounts"
        browser.close()


def test_advisory_board_includes_selahaddin_karatas(server):
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(server + "/team", wait_until="networkidle")
        card = page.locator("article").filter(has_text="Selahaddin Karatas")
        assert card.get_by_role("link", name="LinkedIn").get_attribute("href") == "https://www.linkedin.com/in/sekarsf/"
        assert card.get_by_role("link", name="Website").get_attribute("href") == "https://saaspass.com"
        browser.close()


def test_health_and_legacy_redirect(server):
    import urllib.request
    assert b'"status":"ok"' in urllib.request.urlopen(server + "/healthz").read()
    assert urllib.request.urlopen(server + "/static/site.css").status == 200
    assert urllib.request.urlopen(server + "/static/favicon.svg").status == 200
    response = urllib.request.urlopen(server + "/platform")
    assert response.url.endswith("/products")
