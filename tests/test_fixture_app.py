from pathlib import Path

from examples.fixture_app import _default_static_base_for_output, build_fixture_config, render_fixture_page


def test_fixture_uses_public_personacore_config_name():
    config = build_fixture_config()

    assert config.brand_name == "Example Persona"
    assert config.nav_badges["review"] == 4
    assert config.nav_badges["people"] == 3
    assert config.features["people"] is True
    assert config.features["operations"] is True
    assert config.features["persona"] is True
    assert config.features["agent_ops"] is True
    assert config.features["journal"] is True
    assert config.live_interval == 30


def test_fixture_renders_shared_shell_with_generic_data():
    html = render_fixture_page(static_base_url="/static-fixture")

    assert "Admin Overview" in html
    assert "Example Persona" in html
    assert "pc-dashboard-overview" in html
    assert "Operator Attention" in html
    assert "pc-people-surface" in html
    assert "Example Consumer" in html
    assert "Owner-private notes are summarized for operators." in html
    assert "raw fixture private people note" not in html
    assert "pc-review-surface" in html
    assert "Decision Board" in html
    assert "Owner-private review summary withheld for operators." in html
    assert "Owner-private queue summarized for operators." in html
    assert "raw fixture private review summary" not in html
    assert "raw fixture private queue summary" not in html
    assert "pc-journal-surface" in html
    assert "pc-journal-theme-paper" in html
    assert "A steady day in the runtime" in html
    assert "pc-journal-theme-swatch-matrix" in html
    assert "pc-operations-surface" in html
    assert "Review pending replies" in html
    assert "Owner-private log line summarized for operators." in html
    assert "raw fixture private log line" not in html
    assert "Settings Posture" in html
    assert "pc-persona-surface" in html
    assert "Owner-private persona state summarized for operators." in html
    assert "Owner-private continuity item summarized for operators." in html
    assert "raw fixture private persona" not in html
    assert "pc-agent-ops-surface" in html
    assert "Owner-private agent session summarized for operators." in html
    assert "raw fixture private agent" not in html
    assert "Adapter health" in html
    assert "pc-adapter-health" in html
    assert "pc-message-surface" in html
    assert "pc-message-controls" in html
    assert "Raw rows" in html
    assert "Selected conversation" in html
    assert "pc-activity-surface" in html
    assert "pc-media-surface" in html
    assert "Owner-private reply summarized for operators." in html
    assert "raw fixture owner private message" not in html
    assert "/media/raw-private-fixture" not in html
    assert "Token Health" in html
    assert "Webhook verify token" in html
    assert "/static-fixture/persona-console.css" in html
    assert "Example Persona" in html
    assert "Operator" in html


def test_fixture_static_output_path_points_to_shared_assets(tmp_path):
    output = tmp_path / "fixture.html"

    static_base = _default_static_base_for_output(output)

    assert static_base.endswith(str(Path("src") / "persona_console" / "static"))
