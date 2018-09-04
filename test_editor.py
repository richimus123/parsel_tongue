# coding=utf-8
"""Unit tests for editor."""

import pytest

import editor


@pytest.mark.parametrize('keyword', ['line', 'function', 'variable'])
@pytest.mark.parametrize('text', sorted(editor.SYNONYMS.keys()), ids=sorted(editor.SYNONYMS.keys()))
def test_get_action_from_text_syn(text, keyword):
    """Test getting actions based upon input text when they are keywords in editor.SYNONYMS."""
    result = editor._get_action_from_text(text, keyword=keyword)
    name = result.__name__ if result else None
    if not name:
        # Some of these will return None, because there is function for things like 'yes'.
        pass
    else:
        assert hasattr(editor, name)


@pytest.fixture(autouse=True)
def mock_get_user_input(monkeypatch):
    """Patch the listener to return text instead of requiring user verbal input."""
    monkeypatch.setattr(editor.listener, 'get_user_input', lambda text, **kwargs: text)


@pytest.fixture(autouse=True)
def mock_status_update(monkeypatch):
    """Patch _status_update so it just returns text instead of printing/saying it out loud."""
    monkeypatch.setattr(editor, '_status_update', lambda text: text)


@pytest.mark.parametrize('text, expected', [['ye', True], ['yes', True], ['ya', True], ['yeah', True], ['sure', True],
                                            ['ok', True], ['okay', True], ['nope', False], ['no', False]])
def test_get_yes_or_no(text, expected):
    """Test getting a yes or no response."""
    result = editor._get_yes_or_no(text)
    assert result == expected


@pytest.mark.parametrize('options, expected', [[['a', 'b', 'c'], {'1) a', '2) b', '3) c'}]])
def test_get_help(options, expected):
    """Test _get_help."""
    result = editor._get_help({item: None for item in sorted(options)})
    assert result == sorted(expected)


# TODO: Need tests for: _run_menu, _var_exists, new_function, new_variable, new_line (edit/delete/display/save).
