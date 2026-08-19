from __future__ import annotations

from .models import (
    V2ConsoleConfig,
    V2HeroMedia,
    V2NavItem,
    V2OperatorContext,
    V2PrivacyContext,
    V2Section,
    V2ThemeTokens,
)
from .render import render_v2_console_page


def build_v2_fixture_config(*, owner: bool = False) -> V2ConsoleConfig:
    privacy = V2PrivacyContext(role="owner" if owner else "operator", can_view_owner_only=owner)
    return V2ConsoleConfig(
        brand_name="Example Persona",
        page_title="Today",
        page_subtitle="At-a-glance runtime state",
        active_section="today",
        theme=V2ThemeTokens(name="example-cyan"),
        hero=V2HeroMedia(),
        operator=V2OperatorContext(
            display_name="Example Operator",
            username="operator",
            role=privacy.role,
            read_only=False,
        ),
        privacy=privacy,
        nav_items=(
            V2NavItem("today", "Today", "/", "T"),
            V2NavItem("conversations", "Conversations", "/conversations", "C", badge=3),
            V2NavItem("people", "People", "/people", "P"),
            V2NavItem("mind", "Mind", "/mind", "M"),
            V2NavItem("journal", "Journal", "/journal", "J"),
            V2NavItem("media", "Media", "/media", "A"),
            V2NavItem("persona", "Persona", "/persona", "I"),
            V2NavItem("integrations", "Integrations", "/integrations", "B"),
            V2NavItem("control", "Control", "/control", "O"),
        ),
        status_badges=({"label": "healthy", "tone": "good"},),
        sections=(
            V2Section(
                key="today",
                title="Today",
                subtitle="Current activity, mood, thought, adapters, and newest events.",
                layout="dashboard",
                cards=(
                    {
                        "label": "Current mood",
                        "value": "focused",
                        "detail": "Hover can expose numeric score; click opens the full breakdown.",
                        "tone": "good",
                        "href": "/mind#mood",
                    },
                    {
                        "label": "Current activity",
                        "value": "writing",
                        "detail": "Started 42m ago, projected to wrap around the next scheduled pause.",
                        "tone": "info",
                        "href": "/mind#activity",
                    },
                    {
                        "label": "Owner locked",
                        "value": "private",
                        "detail": "Visible only when the viewer has owner access.",
                        "tone": "owner",
                        "private": {
                            "text": "Raw owner-only fixture detail.",
                            "safe_alternate": "Operator-safe owner-lock summary.",
                            "owner_only": True,
                            "locked": True,
                        },
                    },
                ),
                panels=(
                    {
                        "title": "Most recent thought",
                        "body": "That lunch was better than expected, and I still have work to finish tonight.",
                        "href": "/mind#thoughts",
                        "tone": "cool",
                    },
                ),
                exchanges=(
                    {
                        "user_common_name": "Example Friend",
                        "platform_label": "Discord",
                        "platform": "discord",
                        "direction": "inbound",
                        "persona_name": "Example Persona",
                        "relative_time": "5m ago",
                        "timestamp": "Today 9:41 PM",
                        "message": "DM from Example Friend: opened the conversation thread.",
                        "href": "/conversations/example",
                    },
                ),
                feed=(
                    {
                        "icon": "J",
                        "provider": "journal",
                        "when": "7m ago",
                        "title": "Journal entry",
                        "detail": "Tagged with work, mood, and reflection.",
                        "href": "/journal/latest",
                    },
                ),
            ),
            V2Section(
                key="people",
                title="People",
                subtitle="Social profile directory shape.",
                layout="people",
                search_placeholder="Search people, tags, providers",
                columns=(
                    {"key": "name", "label": "Name"},
                    {"key": "score", "label": "Relationship"},
                    {"key": "tags", "label": "Tags"},
                    {"key": "providers", "label": "Platforms"},
                ),
                rows=(
                    {
                        "cells": {
                            "name": "Example Person",
                            "score": "attached / warm",
                            "tags": "friend, creator, music",
                            "providers": "Discord, Instagram",
                        },
                        "href": "/people/example",
                    },
                ),
            ),
            V2Section(
                key="conversations",
                title="Conversation Thread",
                subtitle="Provider-themed thread shape.",
                layout="conversation",
                panels=(
                    {"title": "Example Friend", "body": "Latest DM, warm relationship", "href": "/conversations/example"},
                ),
                messages=(
                    {"author": "Example Friend", "body": "You around?", "side": "left", "when": "9:41 PM"},
                    {"author": "Example Persona", "body": "Yeah, just finishing something.", "side": "right", "when": "9:42 PM"},
                ),
            ),
            V2Section(
                key="media",
                title="Media",
                subtitle="Instagram-style asset wall.",
                layout="media",
                media=(
                    {"title": "Missing image", "caption": "Generic placeholder until runtime supplies media."},
                    {
                        "title": "Owner-only media",
                        "caption": "Hidden from operators.",
                        "private": True,
                        "tone": "owner",
                    },
                ),
            ),
        ),
    )


def render_v2_fixture_page(*, owner: bool = False) -> str:
    return render_v2_console_page(build_v2_fixture_config(owner=owner))
