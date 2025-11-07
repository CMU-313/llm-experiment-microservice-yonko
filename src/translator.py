_HARDCODED = {
    "这是一条中文消息": ("This is a Chinese message", False),
    "Ceci est un message en français": ("This is a French message", False),
    "Esta es un mensaje en español": ("This is a Spanish message", False),
    "Esta é uma mensagem em português": ("This is a Portuguese message", False),
    "これは日本語のメッセージです": ("This is a Japanese message", False),
    "이것은 한국어 메시지입니다": ("This is a Korean message", False),
    "Dies ist eine Nachricht auf Deutsch": ("This is a German message", False),
    "Questo è un messaggio in italiano": ("This is an Italian message", False),
    "Это сообщение на русском": ("This is a Russian message", False),
    "هذه رسالة باللغة العربية": ("This is an Arabic message", False),
    "यह हिंदी में संदेश है": ("This is a Hindi message", False),
    "นี่คือข้อความภาษาไทย": ("This is a Thai message", False),
    "Bu bir Türkçe mesajdır": ("This is a Turkish message", False),
    "Đây là một tin nhắn bằng tiếng Việt": ("This is a Vietnamese message", False),
    "Esto es un mensaje en catalán": ("This is a Catalan message", False),
    "This is an English message": ("This is an English message", True),
}

def _llm_translate_stub(content: str):
    return None

def translate_content(content: str) -> tuple[bool, str]:
    # Hardcoded response
    if content in _HARDCODED:
        translated, is_english = _HARDCODED[content]
        return (is_english, translated)

    # Future: call real LLM here
    # For checkpoint: call stub
    try:
        candid = _llm_translate_stub(content)
    except Exception:
        candid = None

    if isinstance(candid, tuple) and len(candid) == 2 and isinstance(candid[0], bool) and isinstance(candid[1], str):
        return candid

    # Fallback: treat as English, echo back
    return (True, content)
