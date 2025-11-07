from unittest.mock import patch
import pytest

# Import the function under test
# from your_module import query_llm_robust


@patch("__main__.get_translation", side_effect=Exception("Server timeout"))
def test_translation_server_timeout(mock_translation):
    """ Translation call raises an exception (e.g., timeout or network error)."""
    success, message = query_llm_robust("Bonjour le monde")

    assert success is False
    assert "Error during translation" in message
    assert "Server timeout" in message


@patch("__main__.get_translation")
@patch("__main__.get_language", side_effect=Exception("500 Internal Server Error"))
def test_language_server_error(mock_language, mock_translation):
    """Language detection call fails due to server error."""
    mock_translation.return_value = "Hello world!"

    success, message = query_llm_robust("Hola mundo")

    assert success is False
    assert "Error during language detection" in message
    assert "500 Internal Server Error" in message


@patch("__main__.get_translation")
@patch("__main__.get_language")
def test_language_returns_none(mock_language, mock_translation):
    """ Language API returns None — should produce a graceful failure message."""
    mock_translation.return_value = "Hello again!"
    mock_language.return_value = None

    success, message = query_llm_robust("Ciao mondo")

    assert success is False
    assert message == "Error: No language detected"


@patch("__main__.get_translation", return_value="ERROR555")
@patch("__main__.get_language")
def test_translation_returns_error_code(mock_language, mock_translation):
    """ Translation API responds with explicit error code."""
    mock_language.return_value = "french"

    success, message = query_llm_robust("Salut tout le monde")

    assert success is False
    assert "Error: Could not translate the text" in message
