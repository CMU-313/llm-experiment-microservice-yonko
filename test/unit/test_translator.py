from src.translator import translate_content

def test_known_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_known_english():
    is_english, translated = translate_content("This is an English message")
    assert is_english is True
    assert translated == "This is an English message"

def test_unknown_fallback():
    text = "Random unknown text 123"
    is_english, translated = translate_content(text)
    assert is_english is True
    assert translated == text

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass
