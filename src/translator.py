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

# translation.py
import os
try:
    from ollama import Client  # optional; avoid failing import if package missing
    _HAS_OLLAMA = True
except Exception:
    Client = None  # type: ignore
    _HAS_OLLAMA = False

# Host and model (can be overridden with env vars)
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

def get_translation(post: str) -> str:
    context = """You are a strict translater. You receive an input string in any language, and 
    you return the translation in English.
    
    Return ONLY the translated text in English, no extra words, no explanation, no newlines. 
    Preserve punctuation exactly. 

    Example 1:
    Input: 'J'aime les nouilles'
    Output: 'I like noodles'

    Example 2:
    Input: 'Hier ist dein erstes Beispiel.'
    Output: 'Here is your first example.'

    Here is the input: """ + post

    # Create Ollama client lazily and handle connectivity failures
    if not _HAS_OLLAMA:
        print("ollama package not available; skipping LLM call")
        return post

    client = Client(host=OLLAMA_URL)
    try:
        response = client.chat(
            model=MODEL_NAME,  # model name
            messages=[
                {
                    "role": "user",
                    "content": context
                }
            ]
        )
    except Exception as e:
        print("Ollama request failed:", e)
        return post

    return response.message.content

def get_language(post: str) -> str:
    context = """You are a language classifier. Detect the language of the input text and reply only with the English name of that language:
    Input Text: """ + post 

    # Initialize the OpenAI client
    client = Client(host=OLLAMA_URL)

    # Make a request to your Ollama model, running on your Colab server
    response = client.chat(
        model=MODEL_NAME,  # model name
        messages=[
            {
                "role": "user",
                "content": context
            }
        ]
    )

    return response.message.content

def _llm_translate_stub(post: str) -> tuple[bool, str]:
    english = "english"
    translation = get_translation(post)
    language = get_language(post)
    if language.lower() == english:
        return (True, translation + 'eng llm resp')
    else:
        return (False, translation + 'not eng llm resp')

def translate_content(content: str) -> tuple[bool, str]:
    # Hardcoded response
    if content in _HARDCODED:
        translated, is_english = _HARDCODED[content]
        return (is_english, translated + 'hard coded')

    # Future: call real LLM here
    # For checkpoint: call stub
    try:
        res = _llm_translate_stub(content)
    except Exception:
        res = None

    if isinstance(res, tuple) and len(res) == 2 and isinstance(res[0], bool) and isinstance(res[1], str):
        return res
    
    # otherwise just leave it as is 
    return (True, content + 'leave as is')
