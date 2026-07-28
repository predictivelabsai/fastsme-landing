"""Browser smoke tests for the FastSME landing site."""

import socket
import subprocess
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
        [str(ROOT / ".venv" / "bin" / "python"), "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(PORT)],
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
        assert page.locator("text=Predictive Labs").count() == 0
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


def test_health_and_legacy_redirect(server):
    import urllib.request
    assert b'"status":"ok"' in urllib.request.urlopen(server + "/healthz").read()
    assert urllib.request.urlopen(server + "/static/site.css").status == 200
    assert urllib.request.urlopen(server + "/static/favicon.svg").status == 200
    response = urllib.request.urlopen(server + "/platform")
    assert response.url.endswith("/products")
