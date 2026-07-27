"""Carga y validación de presets, profiles y addons desde TOML (stdlib tomllib)."""
from __future__ import annotations

import tomllib
from pathlib import Path

from framework.model import ConfigError

_PRESET_KEYS = {"stack", "language", "commands", "structure", "skills", "precommit", "maturity"}
_PROFILE_KEYS = {"profile", "agents", "git_host", "ci", "ticket_format", "branch_pattern"}
_ADDON_KEYS = {"addon", "skills"}
_VALID_MATURITY = {"real", "plantilla-base"}


def available(directory: Path) -> list[str]:
    if not directory.exists():
        return []
    return sorted(p.name for p in directory.iterdir() if p.is_dir())


def _load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _require(data: dict, keys: set[str], what: str) -> None:
    missing = keys - data.keys()
    if missing:
        raise ConfigError(f"{what} incompleto, faltan claves: {', '.join(sorted(missing))}")


def load_preset(presets_dir: Path, stack: str) -> dict:
    path = presets_dir / stack / "preset.toml"
    if not path.exists():
        raise ConfigError(
            f"stack '{stack}' no existe. Disponibles: {', '.join(available(presets_dir))}"
        )
    data = _load_toml(path)
    _require(data, _PRESET_KEYS, f"preset '{stack}'")
    if data["maturity"] not in _VALID_MATURITY:
        raise ConfigError(
            f"preset '{stack}': maturity '{data['maturity']}' inválido "
            f"(usar {' o '.join(sorted(_VALID_MATURITY))})"
        )
    return data


def load_profile(profiles_dir: Path, name: str) -> dict:
    path = profiles_dir / f"{name}.toml"
    if not path.exists():
        names = sorted(p.stem for p in profiles_dir.glob("*.toml"))
        raise ConfigError(f"profile '{name}' no existe. Disponibles: {', '.join(names)}")
    data = _load_toml(path)
    _require(data, _PROFILE_KEYS, f"profile '{name}'")
    return data


def load_addon(addons_dir: Path, name: str) -> dict:
    path = addons_dir / name / "addon.toml"
    if not path.exists():
        raise ConfigError(
            f"addon '{name}' no existe. Disponibles: {', '.join(available(addons_dir))}"
        )
    data = _load_toml(path)
    _require(data, _ADDON_KEYS, f"addon '{name}'")
    return data
