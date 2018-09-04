# coding=utf-8
"""Unit tests for editor."""

import pytest

import editor

# TODO: Better testing, py-yaml + coverage + perf, etc.
# TODO: Mock input audio to text for simpler testing!!!


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
