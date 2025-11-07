import src.translator as tr

def test_stub_success_non_english(monkeypatch):
    """Stub returns a valid non-English tuple, service passes it through."""
    def fake_stub(content: str):
        return (False, "Fake translated")
    monkeypatch.setattr(tr, "_llm_translate_stub", fake_stub)

    is_english, translated = tr.translate_content("Bonjour le monde")
    assert is_english is False
    assert translated == "Fake translated"

def test_stub_success_english(monkeypatch):
    """Stub returns a valid English tuple, service passes it through."""
    def fake_stub(content: str):
        return (True, "Already English")
    monkeypatch.setattr(tr, "_llm_translate_stub", fake_stub)

    is_english, translated = tr.translate_content("Hello world")
    assert is_english is True
    assert translated == "Already English"

def test_stub_gibberish_shape(monkeypatch):
    """Stub returns a bad shape, service falls back to echo-as-English."""
    def fake_stub(content: str):
        return "not-a-tuple"
    monkeypatch.setattr(tr, "_llm_translate_stub", fake_stub)

    text = "unmapped input"
    is_english, translated = tr.translate_content(text)
    assert is_english is True
    assert translated == text

def test_stub_exception(monkeypatch):
    """Stub raises exception, service falls back to echo-as-English."""
    def fake_stub(content: str):
        raise RuntimeError("Server timeout")
    monkeypatch.setattr(tr, "_llm_translate_stub", fake_stub)

    text = "another unmapped input"
    is_english, translated = tr.translate_content(text)
    assert is_english is True
    assert translated == text
