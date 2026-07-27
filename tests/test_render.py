import pytest

from framework.render import (
    UnresolvedPlaceholderError,
    find_unresolved,
    render,
)


def test_render_substitutes_known_placeholders():
    out = render("Lenguaje: ${language}", {"language": "Python 3.12+"})
    assert out == "Lenguaje: Python 3.12+"


def test_render_escaped_dollar_is_literal():
    out = render("usa $$HOME en shell", {})
    assert out == "usa $HOME en shell"


def test_find_unresolved_lists_missing():
    assert find_unresolved("a ${x} b ${y} ${x}") == ["x", "y"]


def test_render_raises_on_unresolved():
    with pytest.raises(UnresolvedPlaceholderError) as exc:
        render("hola ${falta}", {}, source="core/x.md")
    assert exc.value.placeholders == ["falta"]
    assert exc.value.source == "core/x.md"
