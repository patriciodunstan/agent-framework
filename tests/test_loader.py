from pathlib import Path

import pytest

from framework.loader import available, load_addon, load_preset, load_profile
from framework.model import ConfigError

FIX = Path(__file__).parent / "fixtures"


def test_load_preset_ok():
    p = load_preset(FIX / "presets", "demo")
    assert p["stack"] == "demo"
    assert p["commands"]["test"] == "demo test"


def test_load_preset_unknown_lists_available():
    with pytest.raises(ConfigError) as exc:
        load_preset(FIX / "presets", "noexiste")
    assert "demo" in str(exc.value)


def test_load_preset_missing_key(tmp_path):
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "preset.toml").write_text('stack = "bad"\n', encoding="utf-8")
    with pytest.raises(ConfigError):
        load_preset(tmp_path, "bad")


def test_load_profile_ok():
    pr = load_profile(FIX / "profiles", "demo")
    assert pr["git_host"] == "github"


def test_load_addon_ok():
    a = load_addon(FIX / "addons", "demo")
    assert a["skills"] == ["demo-addon-skill"]


def test_available_sorted():
    assert available(FIX / "presets") == ["demo"]
