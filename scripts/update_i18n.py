#!/usr/bin/env python3
"""Inventory, check, and optionally refresh FastSME locale catalogues.

Translation is an explicit maintenance operation; deployed requests only read the
checked-in JSON catalogues and never call an external service.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from components import NAV, SITE_TAGLINE  # noqa: E402
from content.clients import CLIENTS  # noqa: E402
from content.partners import PARTNERS  # noqa: E402
from content.products import GROUPS  # noqa: E402
from content.team import ADVISORY, TEAM  # noqa: E402
from utils.i18n import DEFAULT_LANG, LANGUAGES, LOCALES_DIR  # noqa: E402


TRANSLATING_CALLS = {"t", "T", "Button_", "page"}

MANUAL_OVERRIDES = {
    "et": ["Tooted", "Kliendid", "Partnerid", "Avatud lähtekood", "Tees", "Meeskond", "Logi sisse", "Sisse logitud", "Võta ühendust", "Kontakt", "Vali keel", "Ava või sulge menüü", "Tutvu", "Meie tees", "Põhimeeskond", "Nõukoda", "Integratsioonipartnerid", "Toetab Predictive Labs Ltd"],
    "de": ["Produkte", "Kunden", "Partner", "Open Source", "These", "Team", "Anmelden", "Angemeldet", "Kontakt aufnehmen", "Kontakt", "Sprache wählen", "Navigation ein-/ausblenden", "Entdecken", "Unsere These", "Kernteam", "Beirat", "Integrationspartner", "Bereitgestellt von Predictive Labs Ltd"],
    "fr": ["Produits", "Clients", "Partenaires", "Open source", "Vision", "Équipe", "Se connecter", "Connecté", "Nous contacter", "Contact", "Choisir la langue", "Ouvrir ou fermer la navigation", "Découvrir", "Notre vision", "Équipe principale", "Conseil consultatif", "Partenaires d’intégration", "Propulsé par Predictive Labs Ltd"],
    "sv": ["Produkter", "Kunder", "Partner", "Öppen källkod", "Tes", "Team", "Logga in", "Inloggad", "Kontakta oss", "Kontakt", "Välj språk", "Visa/dölj navigation", "Utforska", "Vår tes", "Kärnteam", "Rådgivande styrelse", "Integrationspartner", "Drivs av Predictive Labs Ltd"],
    "lv": ["Produkti", "Klienti", "Partneri", "Atvērtais pirmkods", "Tēze", "Komanda", "Pierakstīties", "Jūs esat pierakstījies", "Sazinieties ar mums", "Kontakti", "Izvēlēties valodu", "Atvērt/aizvērt navigāciju", "Izpētīt", "Mūsu tēze", "Pamatkomanda", "Padomdevēju padome", "Integrācijas partneri", "Nodrošina Predictive Labs Ltd"],
    "no": ["Produkter", "Kunder", "Partnere", "Åpen kildekode", "Tese", "Team", "Logg inn", "Innlogget", "Kontakt oss", "Kontakt", "Velg språk", "Vis/skjul navigasjon", "Utforsk", "Vår tese", "Kjerneteam", "Rådgivende styre", "Integrasjonspartnere", "Drevet av Predictive Labs Ltd"],
    "da": ["Produkter", "Kunder", "Partnere", "Open source", "Tese", "Team", "Log ind", "Logget ind", "Kontakt os", "Kontakt", "Vælg sprog", "Vis/skjul navigation", "Udforsk", "Vores tese", "Kerneteam", "Rådgivende udvalg", "Integrationspartnere", "Drevet af Predictive Labs Ltd"],
    "pl": ["Produkty", "Klienci", "Partnerzy", "Open source", "Teza", "Zespół", "Zaloguj się", "Zalogowano", "Porozmawiaj z nami", "Kontakt", "Wybierz język", "Pokaż/ukryj nawigację", "Odkryj", "Nasza teza", "Główny zespół", "Rada doradcza", "Partnerzy integracyjni", "Obsługiwane przez Predictive Labs Ltd"],
    "nl": ["Producten", "Klanten", "Partners", "Open source", "Visie", "Team", "Inloggen", "Ingelogd", "Neem contact op", "Contact", "Kies taal", "Navigatie tonen/verbergen", "Ontdek", "Onze visie", "Kernteam", "Adviesraad", "Integratiepartners", "Mogelijk gemaakt door Predictive Labs Ltd"],
    "fi": ["Tuotteet", "Asiakkaat", "Kumppanit", "Avoin lähdekoodi", "Teesi", "Tiimi", "Kirjaudu sisään", "Kirjautunut", "Ota yhteyttä", "Yhteystiedot", "Valitse kieli", "Näytä/piilota navigointi", "Tutustu", "Teesimme", "Ydintiimi", "Neuvonantajat", "Integraatiokumppanit", "Taustalla Predictive Labs Ltd"],
    "lt": ["Produktai", "Klientai", "Partneriai", "Atvirasis kodas", "Tezė", "Komanda", "Prisijungti", "Prisijungta", "Susisiekite", "Kontaktai", "Pasirinkti kalbą", "Rodyti/slėpti navigaciją", "Sužinoti daugiau", "Mūsų tezė", "Pagrindinė komanda", "Patarėjų taryba", "Integracijos partneriai", "Teikia Predictive Labs Ltd"],
}

OVERRIDE_KEYS = [
    "Products", "Clients", "Partners", "Open source", "Thesis", "Team",
    "Sign In", "Signed in", "Talk to us", "Contact", "Choose language",
    "Toggle navigation", "Explore", "Our thesis", "Core team",
    "Advisory board", "Integration partners", "Powered by Predictive Labs Ltd",
]
MANUAL_OVERRIDES = {
    lang: dict(zip(OVERRIDE_KEYS, translations, strict=True))
    for lang, translations in MANUAL_OVERRIDES.items()
}


def _translation_literals(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.IfExp):
        return _translation_literals(node.body) + _translation_literals(node.orelse)
    return []


def source_strings() -> set[str]:
    strings = {SITE_TAGLINE, *(label for label, _ in NAV)}
    for path in (ROOT / "app.py", ROOT / "components.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else None
            if name in TRANSLATING_CALLS:
                strings.update(_translation_literals(node.args[0]))
            elif name == "enumerate":
                strings.update(
                    child.value for child in ast.walk(node.args[0])
                    if isinstance(child, ast.Constant) and isinstance(child.value, str)
                )
    for group in GROUPS:
        strings.update((group["name"], group["description"]))
        for _, label, description in group["products"]:
            strings.update((label, description))
    for _, sector, description in CLIENTS:
        strings.update((sector, description))
    strings.update(partner["description"] for partner in PARTNERS)
    for person in (*TEAM, *ADVISORY):
        strings.update((person["role"], person["bio"]))
    return {value for value in strings if value and value not in {"en", "/"}}


def read_catalog(lang: str) -> dict[str, str]:
    path = LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise ValueError(f"{path} must contain a string-to-string JSON object")
    return data


def check_catalogs() -> bool:
    source = source_strings()
    valid = True
    for lang in LANGUAGES:
        if lang == DEFAULT_LANG:
            continue
        catalog = read_catalog(lang)
        missing = sorted(source - catalog.keys())
        stale = sorted(catalog.keys() - source)
        empty = sorted(key for key, value in catalog.items() if not value.strip())
        if missing or stale or empty:
            valid = False
            print(f"{lang}: {len(missing)} missing, {len(stale)} stale, {len(empty)} empty")
            for label, values in (("missing", missing), ("stale", stale), ("empty", empty)):
                for value in values[:10]:
                    print(f"  {label}: {value}")
        else:
            print(f"{lang}: {len(catalog)} translations complete")
    return valid


def _translate_one(text: str, lang: str) -> str:
    query = urlencode({"client": "gtx", "sl": "en", "tl": lang, "dt": "t", "q": text})
    request = Request(
        f"https://translate.googleapis.com/translate_a/single?{query}",
        headers={"User-Agent": "FastSME translation maintenance/1.0"},
    )
    for attempt in range(4):
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read())
            translated = "".join(part[0] for part in payload[0] if part and part[0]).strip()
            if translated:
                return translated
        except Exception:
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Translation failed for {lang}: {text}")


def refresh_catalogs(workers: int) -> None:
    LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    source = source_strings()
    for lang in LANGUAGES:
        if lang == DEFAULT_LANG:
            continue
        current = read_catalog(lang)
        catalog = {key: current[key] for key in source if key in current and current[key].strip()}
        missing = sorted(source - catalog.keys())
        print(f"{lang}: translating {len(missing)} of {len(source)} strings")
        if missing:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(_translate_one, text, lang): text for text in missing}
                for index, future in enumerate(as_completed(futures), 1):
                    text = futures[future]
                    catalog[text] = future.result()
                    if index % 25 == 0 or index == len(missing):
                        print(f"  {index}/{len(missing)}")
        catalog.update(MANUAL_OVERRIDES[lang])
        path = LOCALES_DIR / f"{lang}.json"
        path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--translate", action="store_true", help="translate missing source copy and rewrite catalogues")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if args.translate:
        refresh_catalogs(max(1, args.workers))
    return 0 if check_catalogs() else 1


if __name__ == "__main__":
    raise SystemExit(main())
