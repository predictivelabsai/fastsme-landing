"""Translation catalogue and language-selection unit tests."""

from types import SimpleNamespace

from scripts.update_i18n import source_strings
from utils.i18n import LANGUAGES, catalog, detect_language, get_lang, set_lang, t


def _request(accept_language=""):
    return SimpleNamespace(headers={"accept-language": accept_language})


def test_all_locale_catalogues_are_complete_and_current():
    expected = source_strings()
    for lang in LANGUAGES:
        if lang == "en":
            continue
        translations = catalog(lang)
        assert translations.keys() == expected
        assert all(value.strip() for value in translations.values())


def test_browser_language_detection_honours_quality_and_region():
    assert detect_language(_request("de-DE,de;q=0.9,en;q=0.8")) == "de"
    assert detect_language(_request("es-ES;q=1,fr-FR;q=0.7")) == "fr"
    assert detect_language(_request("es-ES,zh;q=0.8")) == "en"


def test_session_preference_wins_and_invalid_language_is_ignored():
    session = {}
    assert get_lang(session, _request("fi-FI")) == "fi"
    assert session["lang"] == "fi"
    assert set_lang(session, "lt") == "lt"
    assert set_lang(session, "invalid") == "lt"


def test_english_is_the_safe_translation_fallback():
    source = "A future string that has not been translated yet"
    assert t(source, "en") == source
    assert t(source, "de") == source
    assert t("Products", "de") != "Products"
