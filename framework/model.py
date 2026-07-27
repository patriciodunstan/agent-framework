"""Tipos compartidos por el motor del framework."""
from __future__ import annotations

from dataclasses import dataclass, field


class ConfigError(Exception):
    """Error de configuración de entrada (stack/profile/addon inválido o incompleto)."""


@dataclass(frozen=True)
class OutputFile:
    """Un archivo a escribir, con ruta relativa al destino de instalación."""

    relpath: str
    content: str


@dataclass
class InstallReport:
    """Resultado de una instalación idempotente."""

    created: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
