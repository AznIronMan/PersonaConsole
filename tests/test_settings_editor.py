from personaconsole import (
    SETTINGS_EDITOR_FEATURE,
    FlashBanner,
    SettingsChange,
    SettingsEditorConfig,
    SettingsField,
    SettingsGroup,
    SettingsValidationMessage,
    SurfaceAction,
    render_settings_editor,
    settings_editor_feature_enabled,
)


def test_settings_editor_renders_grouped_fields_changes_and_redacted_secret():
    html = render_settings_editor(
        SettingsEditorConfig(
            enabled=True,
            title="<Runtime Settings>",
            subtitle="Grouped runtime-owned config",
            form_action="/settings/save",
            banners=[FlashBanner("Saved safely", tone="good", action_label="Audit", action_href="/settings/audit")],
            messages=[SettingsValidationMessage("Interval is above normal", field_key="interval", tone="warn")],
            groups=[
                SettingsGroup(
                    "runtime",
                    "Runtime",
                    "Safe display values only",
                    fields=[
                        SettingsField(
                            "provider",
                            "<Provider>",
                            "provider",
                            "select",
                            "openai",
                            options=["openai", "xai"],
                        ),
                        SettingsField(
                            "api-key",
                            "API key",
                            "api_key",
                            "secret",
                            "raw-secret-token",
                            display_value="configured",
                            changed=True,
                            pending_value="new-raw-secret-token",
                            pending_display_value="new secret staged",
                            restart_required=True,
                            actions=[SurfaceAction("Reveal", "/settings/reveal/api-key")],
                        ),
                        SettingsField(
                            "interval",
                            "Interval",
                            "interval",
                            "number",
                            15,
                            pending_value=30,
                            changed=True,
                            min_value=1,
                            max_value=60,
                            step=1,
                        ),
                        SettingsField("notes", "Notes", "notes", "textarea", "hello <operator>"),
                        SettingsField("debug", "Debug", "debug", "boolean", True),
                        SettingsField("payload", "Payload", "payload", "json", {"enabled": True}, readonly=True),
                    ],
                )
            ],
        )
    )

    assert "pc-settings-editor" in html
    assert "&lt;Runtime Settings&gt;" in html
    assert "&lt;Provider&gt;" in html
    assert '<form class="pc-settings-editor' in html
    assert 'action="/settings/save"' in html
    assert '<option value="openai" selected>openai</option>' in html
    assert 'value="30"' in html
    assert "hello &lt;operator&gt;" in html
    assert 'type="checkbox"' in html
    assert "&quot;enabled&quot;: true" in html
    assert "Pending Changes" in html
    assert "restart required" in html
    assert "configured" in html
    assert "/settings/reveal/api-key" in html
    assert "raw-secret-token" not in html
    assert "new-raw-secret-token" not in html
    assert "new secret staged" not in html


def test_settings_editor_explicit_change_redacts_secret_values():
    html = render_settings_editor(
        {
            "enabled": True,
            "changes": [
                SettingsChange(
                    "Webhook secret",
                    before="old raw",
                    after="new raw",
                    secret=True,
                    restart_required=True,
                )
            ],
            "groups": [{"key": "empty", "title": "Empty"}],
        }
    )

    assert "Webhook secret" in html
    assert "********" in html
    assert "old raw" not in html
    assert "new raw" not in html


def test_settings_editor_feature_gate_and_empty_state():
    config = SettingsEditorConfig(enabled=True)

    assert settings_editor_feature_enabled(config, {SETTINGS_EDITOR_FEATURE: True}) is True
    assert settings_editor_feature_enabled(config, {SETTINGS_EDITOR_FEATURE: False}) is False
    assert render_settings_editor(config, features={SETTINGS_EDITOR_FEATURE: False}) == ""

    html = render_settings_editor(config)

    assert "No editable settings configured." in html
