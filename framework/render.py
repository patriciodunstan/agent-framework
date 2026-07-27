"""Render de plantillas con string.Template y detección de placeholders sin resolver."""
from __future__ import annotations

import re
from string import Template

_PLACEHOLDER_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


class UnresolvedPlaceholderError(Exception):
    def __init__(self, placeholders: list[str], source: str) -> None:
        self.placeholders = placeholders
        self.source = source
        super().__init__(
            f"Placeholders sin resolver en {source}: {', '.join(placeholders)}"
        )


def find_unresolved(text: str) -> list[str]:
    """Devuelve los nombres de placeholders ${...} presentes, ordenados y únicos."""
    return sorted(set(_PLACEHOLDER_RE.findall(text)))


def render(text: str, context: dict[str, str], *, source: str = "<texto>") -> str:
    """Sustituye ${var}; falla si queda algún ${...} sin resolver."""
    result = Template(text).safe_substitute(context)
    unresolved = find_unresolved(result)
    if unresolved:
        raise UnresolvedPlaceholderError(unresolved, source)
    return result
