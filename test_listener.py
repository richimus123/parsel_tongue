# coding=utf-8
"""Unit tests for listener."""

import pytest

import listener

# TODO: Need unit tests for: echo, get_user_input, listen_and_transcribe, speak_text, status_update


@pytest.fixture(autouse=True)
def mock_status_update(monkeypatch):
    """Patch the status_update so it doesn't speak/print."""
    monkeypatch.setattr(listener, 'status_update', lambda text: text)


@pytest.mark.parametrize('raw_text, expected_result', [['This is a test', 'test'],
                                                       ['I want to edit a function', 'want edit function'],
                                                       ['', ''],
                                                       ['function', 'function']])
def test_interpret_meaning(raw_text, expected_result):
    """Unit tests for interpret_meaning."""
    result = listener.interpret_meaning(raw_text)
    assert result == expected_result
