from importlib.resources import files
from pathlib import Path

import tomllib


PLACEHOLDER_NAMES = {
    "hero-desktop-missing.svg",
    "hero-mobile-missing.svg",
    "media-tile-missing.svg",
    "provider-icon-missing.svg",
    "document-tile-missing.svg",
    "audio-tile-missing.svg",
}


def test_generic_placeholder_svgs_are_packaged_and_public_safe():
    placeholders = files("personaconsole").joinpath("static", "placeholders")

    for name in PLACEHOLDER_NAMES:
        text = placeholders.joinpath(name).read_text(encoding="utf-8")
        assert "<svg" in text
        assert "Missing" in text or "MISSING" in text
        assert "Jazmine" not in text
        assert "Geon" not in text
        assert "HeartAndSoul" not in text


def test_pyproject_includes_nested_placeholder_static_assets():
    package_data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))[
        "tool"
    ]["setuptools"]["package-data"]["personaconsole"]

    assert "static/placeholders/*.svg" in package_data
