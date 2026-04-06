import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_client import ask_claude


def test_ask_claude_returns_string():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="test response")]
    with patch("claude_client.anthropic_client.messages.create", return_value=mock_response):
        result = ask_claude("system prompt", "user prompt")
    assert isinstance(result, str)
    assert result == "test response"


def test_ask_claude_passes_model_and_tokens():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="ok")]
    with patch("claude_client.anthropic_client.messages.create", return_value=mock_response) as mock_create:
        ask_claude("sys", "user", max_tokens=500)
        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs["max_tokens"] == 500
        assert "system" in call_kwargs
