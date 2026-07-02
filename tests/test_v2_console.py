from pathlib import Path

from personaconsole.v2 import (
    V2ConsoleConfig,
    V2NavItem,
    V2PrivacyContext,
    V2PrivateValue,
    V2Section,
    V2ThemeTokens,
    build_v2_fixture_config,
    render_v2_console_page,
    render_v2_fixture_page,
    render_v2_private_text,
)


def test_v2_imports_and_theme_css_are_public():
    theme = V2ThemeTokens(name="fixture")

    css = theme.css_variables()

    assert "--pcv2-accent" in css
    assert "Orbitron" in css
    assert "Jazmine" not in css
    assert "HeartAndSoul" not in css


def test_v2_shell_renders_hero_nav_sections_and_assets():
    html = render_v2_fixture_page()

    assert "persona-console-v2.css" in html
    assert "persona-console-v2.js" in html
    assert "hero-desktop-missing.svg" in html
    assert "Example Persona" in html
    assert "pcv2-nav-item is-active" in html
    assert "Conversations" in html
    assert "Current mood" in html
    assert "DM from Example Friend" in html
    assert "pcv2-thread" in html
    assert "pcv2-media-grid" in html


def test_v2_owner_lock_uses_safe_alternate_for_operator_and_raw_for_owner():
    value = V2PrivateValue(
        text="raw owner-only fixture detail",
        safe_alternate="operator-safe summary",
        owner_only=True,
        locked=True,
    )

    assert render_v2_private_text(value, V2PrivacyContext(role="operator")) == "operator-safe summary"
    assert render_v2_private_text(value, V2PrivacyContext(role="owner")) == "raw owner-only fixture detail"

    operator_html = render_v2_fixture_page(owner=False)
    owner_html = render_v2_fixture_page(owner=True)

    assert "Operator-safe owner-lock summary." in operator_html
    assert "Raw owner-only fixture detail." not in operator_html
    assert "Raw owner-only fixture detail." in owner_html


def test_v2_config_accepts_mapping_payloads_for_consumer_adapters():
    html = render_v2_console_page(
        {
            "brand_name": "Example Persona",
            "page_title": "People",
            "page_subtitle": "Directory",
            "active_section": "people",
            "theme": {"accent": "#11c5f5", "display_font_stack": "Orbitron, sans-serif"},
            "privacy": {"role": "moderator", "read_only": True},
            "operator": {"display_name": "Read Only", "role": "moderator", "read_only": True},
            "nav_items": [
                {"key": "today", "label": "Today", "href": "/"},
                {"key": "people", "label": "People", "href": "/people"},
            ],
            "sections": [
                {
                    "key": "people",
                    "title": "People",
                    "layout": "people",
                    "search_placeholder": "Search",
                    "columns": [
                        {"key": "name", "label": "Name"},
                        {"key": "score", "label": "Relationship"},
                    ],
                    "rows": [
                        {"cells": {"name": "Example Person", "score": "warm"}, "href": "/people/1"},
                    ],
                }
            ],
        }
    )

    assert 'data-pcv2-role="moderator"' in html
    assert "Read Only" in html
    assert "People" in html
    assert "Example Person" in html
    assert "pcv2-search" in html


def test_v2_linked_table_rows_keep_cells_and_render_actions():
    html = render_v2_console_page(
        {
            "brand_name": "Example Persona",
            "page_title": "People",
            "active_section": "people",
            "nav_items": [{"key": "people", "label": "People", "href": "/people"}],
            "sections": [
                {
                    "key": "people",
                    "title": "People",
                    "layout": "people",
                    "columns": [
                        {"key": "name", "label": "Name"},
                        {"key": "relationship", "label": "Relationship"},
                        {"key": "tags", "label": "Tags"},
                    ],
                    "rows": [
                        {
                            "cells": {
                                "name": "Example Person",
                                "relationship": "friend",
                                "tags": "music, work",
                            },
                            "href": "/people/1",
                            "actions": [
                                {"label": "Patch", "href": "/knowledge-patch?target_surface=person&target_person_id=1"}
                            ],
                        }
                    ],
                }
            ],
        }
    )

    assert '<a href="/people/1">Example Person</a>' in html
    assert "friend" in html
    assert "music, work" in html
    assert "<th>Actions</th>" in html
    assert "/knowledge-patch?target_surface=person&amp;target_person_id=1" in html


def test_v2_media_items_render_actions_without_nesting_tile_anchor():
    html = render_v2_console_page(
        {
            "brand_name": "Example Persona",
            "page_title": "Media",
            "active_section": "media",
            "nav_items": [{"key": "media", "label": "Media", "href": "/media"}],
            "sections": [
                {
                    "key": "media",
                    "title": "Media",
                    "layout": "media",
                    "media": [
                        {
                            "title": "Example Artifact",
                            "caption": "Preview caption",
                            "src": "/placeholder.svg",
                            "href": "/media/1",
                            "actions": [
                                {"label": "Patch", "href": "/knowledge-patch?target_surface=media&target_artifact_id=1"}
                            ],
                        }
                    ],
                }
            ],
        }
    )

    assert '<article class="pcv2-media-tile' in html
    assert 'class="pcv2-media-preview-link" href="/media/1"' in html
    assert "/knowledge-patch?target_surface=media&amp;target_artifact_id=1" in html
    assert '<a class="pcv2-media-tile' not in html


def test_v2_panels_render_actions_without_nesting_panel_anchor():
    html = render_v2_console_page(
        {
            "brand_name": "Example Persona",
            "page_title": "Journal",
            "active_section": "journal",
            "nav_items": [{"key": "journal", "label": "Journal", "href": "/journal"}],
            "sections": [
                {
                    "key": "journal",
                    "title": "Journal",
                    "layout": "cards",
                    "panels": [
                        {
                            "title": "Daily entry",
                            "body": "Full narrative entry.",
                            "href": "/journal#entry-1",
                            "actions": [
                                {"label": "Patch", "href": "/knowledge-patch?target_surface=journal"}
                            ],
                        }
                    ],
                }
            ],
        }
    )

    assert '<article class="pcv2-panel' in html
    assert '<h3><a href="/journal#entry-1">Daily entry</a></h3>' in html
    assert "/knowledge-patch?target_surface=journal" in html
    assert '<a class="pcv2-panel' not in html


def test_v2_can_render_minimal_explicit_models():
    config = V2ConsoleConfig(
        brand_name="Example Persona",
        page_title="Mind",
        active_section="mind",
        theme=V2ThemeTokens(accent="#22d3ee"),
        privacy=V2PrivacyContext(role="operator"),
        nav_items=(V2NavItem(key="mind", label="Mind", href="/mind"),),
        sections=(
            V2Section(
                key="mind",
                title="Mind",
                layout="mind",
                cards=(
                    {
                        "label": "Current mood",
                        "value": "calm",
                        "detail": "Click for the deep dive.",
                    },
                ),
            ),
        ),
    )

    html = render_v2_console_page(config)

    assert "Current mood" in html
    assert "calm" in html
    assert "Click for the deep dive." in html
    assert "pcv2-layout-mind" in html


def test_v2_preserves_long_meaningful_text_and_css_does_not_ellipsis_content():
    long_text = "Full narrative starts. " + ("context sentence " * 80) + "full-narrative-tail"
    html = render_v2_console_page(
        {
            "brand_name": "Example Persona",
            "page_title": "No Truncation",
            "active_section": "today",
            "theme": {},
            "nav_items": [{"key": "today", "label": "Today", "href": "/"}],
            "sections": [
                {
                    "key": "today",
                    "title": "Today",
                    "layout": "dashboard",
                    "panels": [{"title": "Latest thought", "body": long_text}],
                    "feed": [{"title": long_text, "detail": long_text, "when": "now"}],
                },
                {
                    "key": "media",
                    "title": "Media",
                    "layout": "media",
                    "media": [{"title": "Artifact", "caption": long_text, "src": "/placeholder.svg"}],
                },
            ],
        }
    )
    css = Path("src/personaconsole/static/persona-console-v2.css").read_text(encoding="utf-8")

    assert "full-narrative-tail" in html
    assert "text-overflow" not in css
    assert "line-clamp" not in css
