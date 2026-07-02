from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
from html import escape
from typing import Any, Mapping, Sequence, TypeVar

from .models import (
    V2Action,
    V2Badge,
    V2ConsoleConfig,
    V2ConversationMessage,
    V2FeedItem,
    V2HeroMedia,
    V2MediaItem,
    V2MetricCard,
    V2NavItem,
    V2OperatorContext,
    V2Panel,
    V2PrivacyContext,
    V2PrivateValue,
    V2Section,
    V2TableColumn,
    V2TableRow,
    V2ThemeTokens,
)


T = TypeVar("T")


_TONES = {
    "neutral",
    "good",
    "warn",
    "bad",
    "info",
    "owner",
    "operator",
    "moderator",
    "private",
    "muted",
    "hot",
    "cool",
}


def _mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _coerce(value: T | Mapping[str, Any] | str | None, cls: type[T], **defaults: Any) -> T:
    if isinstance(value, cls):
        return value
    if isinstance(value, str):
        data = dict(defaults)
        if cls is V2Badge:
            data["label"] = value
        elif cls is V2Action:
            data["label"] = value
        elif cls is V2PrivateValue:
            data["text"] = value
        else:
            data["title"] = value
        return cls(**data)  # type: ignore[arg-type]
    data = dict(defaults)
    data.update(_mapping(value))
    field_names = {field.name for field in fields(cls)}  # type: ignore[arg-type]
    return cls(**{key: val for key, val in data.items() if key in field_names})  # type: ignore[arg-type]


def _coerce_seq(values: Sequence[Any], cls: type[T], **defaults: Any) -> tuple[T, ...]:
    return tuple(_coerce(value, cls, **defaults) for value in values)


def _tone(value: str) -> str:
    clean = str(value or "neutral").strip().lower().replace("_", "-")
    return clean if clean in _TONES else "neutral"


def _attr(name: str, value: Any, *, boolean: bool = False) -> str:
    if boolean:
        return f" {name}" if value else ""
    if value is None or value == "":
        return ""
    return f' {name}="{escape(str(value), quote=True)}"'


def _safe_id(value: Any, default: str) -> str:
    raw = str(value or "").strip().lower()
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in raw)
    return safe.strip("-_") or default


def _initials(name: str) -> str:
    parts = [part for part in str(name or "").replace("_", " ").replace("-", " ").split() if part]
    if parts:
        return "".join(part[0].upper() for part in parts[:2])
    compact = "".join(char for char in str(name or "") if char.isalnum())
    return compact[:2].upper() or "OP"


def _theme(config: V2ConsoleConfig) -> V2ThemeTokens:
    return _coerce(config.theme, V2ThemeTokens)


def _hero(config: V2ConsoleConfig) -> V2HeroMedia:
    return _coerce(config.hero, V2HeroMedia)


def _operator(config: V2ConsoleConfig) -> V2OperatorContext:
    return _coerce(config.operator, V2OperatorContext)


def _privacy(config: V2ConsoleConfig) -> V2PrivacyContext:
    data = _mapping(config.privacy)
    if config.operator and "read_only" not in data:
        data["read_only"] = _mapping(config.operator).get("read_only", False)
    return _coerce(data, V2PrivacyContext)


def render_v2_private_text(
    value: V2PrivateValue | Mapping[str, Any] | str | None,
    privacy: V2PrivacyContext | Mapping[str, Any] | None = None,
) -> str:
    model = _coerce(value, V2PrivateValue)
    context = _coerce(privacy, V2PrivacyContext)
    if not model.owner_only and not model.locked:
        return model.text
    if context.is_owner:
        return model.text
    if model.safe_alternate:
        return model.safe_alternate
    if model.hide_without_alternate:
        return ""
    return "[owner-only content withheld]"


def _private_attrs(value: V2PrivateValue | Mapping[str, Any] | str | None) -> str:
    if not value:
        return ""
    model = _coerce(value, V2PrivateValue)
    if not model.lockable:
        return ""
    state = "locked" if model.locked or model.owner_only else "available"
    return f' data-pcv2-owner-lock="{state}"'


def _badges(values: Sequence[V2Badge | Mapping[str, Any] | str]) -> str:
    badges = []
    for value in _coerce_seq(values, V2Badge):
        tone = _tone(value.tone)
        title = _attr("title", value.title)
        badges.append(f'<span class="pcv2-badge pcv2-tone-{tone}"{title}>{escape(value.label)}</span>')
    return "".join(badges)


def _actions(values: Sequence[V2Action | Mapping[str, Any] | str]) -> str:
    actions = []
    for value in _coerce_seq(values, V2Action):
        tone = _tone(value.tone)
        icon = f'<span class="pcv2-action-icon" aria-hidden="true">{escape(value.icon)}</span>' if value.icon else ""
        disabled = " is-disabled" if value.disabled else ""
        attrs = _attr("href", value.href if not value.disabled else "#")
        attrs += _attr("title", value.title)
        if value.method.lower() != "get":
            attrs += _attr("data-method", value.method.lower())
        actions.append(
            f'<a class="pcv2-action pcv2-tone-{tone}{disabled}"{attrs}>{icon}<span>{escape(value.label)}</span></a>'
        )
    return "".join(actions)


def _render_card(value: V2MetricCard | Mapping[str, Any], privacy: V2PrivacyContext) -> str:
    card = _coerce(value, V2MetricCard)
    title = card.title or card.label
    label = render_v2_private_text(card.private, privacy) if card.private else card.label
    detail = render_v2_private_text(card.private, privacy) if card.private else card.detail
    if card.private and not label and not detail:
        return ""
    tag = "a" if card.href else "article"
    href = _attr("href", card.href)
    icon = f'<span class="pcv2-card-icon" aria-hidden="true">{escape(card.icon)}</span>' if card.icon else ""
    meta_html = "".join(
        f'<span><b>{escape(str(item.get("label") or ""))}</b>{escape(str(item.get("value") or ""))}</span>'
        for item in card.meta
        if str(item.get("label") or item.get("value") or "").strip()
    )
    return (
        f'<{tag} class="pcv2-card pcv2-tone-{_tone(card.tone)}"{href}{_attr("title", title)}{_private_attrs(card.private)}>'
        f'<div class="pcv2-card-kicker">{icon}<span>{escape(label)}</span>{_badges(card.badges)}</div>'
        f'<strong>{escape(card.value)}</strong>'
        f'<p>{escape(detail)}</p>'
        f'<div class="pcv2-card-meta">{meta_html}</div>'
        f'</{tag}>'
    )


def _render_feed_item(value: V2FeedItem | Mapping[str, Any], privacy: V2PrivacyContext) -> str:
    item = _coerce(value, V2FeedItem)
    title = render_v2_private_text(item.private, privacy) if item.private else item.title
    detail = render_v2_private_text(item.private, privacy) if item.private else item.detail
    if item.private and not title and not detail:
        return ""
    tag = "a" if item.href else "article"
    href = _attr("href", item.href)
    icon = escape(item.icon or item.provider[:1].upper() or "•")
    media_html = "".join(
        f'<span class="pcv2-feed-media">{escape(str(media.get("label") or media.get("kind") or "media"))}</span>'
        for media in item.media
    )
    return (
        f'<{tag} class="pcv2-feed-item pcv2-tone-{_tone(item.tone)}"{href}{_private_attrs(item.private)}>'
        f'<span class="pcv2-feed-icon" aria-hidden="true">{icon}</span>'
        '<span class="pcv2-feed-copy">'
        f'<strong>{escape(title)}</strong>'
        f'<em>{escape(detail)}</em>'
        f'<span>{escape(item.when)}{(" · " + escape(item.provider)) if item.provider else ""}</span>'
        f'</span><span class="pcv2-feed-side">{_badges(item.badges)}{media_html}</span></{tag}>'
    )


def _render_panel(value: V2Panel | Mapping[str, Any], privacy: V2PrivacyContext) -> str:
    panel = _coerce(value, V2Panel)
    body = render_v2_private_text(panel.private, privacy) if panel.private else panel.body
    if panel.private and not body:
        return ""
    tag = "a" if panel.href else "article"
    href = _attr("href", panel.href)
    icon = f'<span class="pcv2-panel-icon" aria-hidden="true">{escape(panel.icon)}</span>' if panel.icon else ""
    return (
        f'<{tag} class="pcv2-panel pcv2-tone-{_tone(panel.tone)}"{href}{_private_attrs(panel.private)}>'
        f'<div class="pcv2-panel-head">{icon}<h3>{escape(panel.title)}</h3>{_badges(panel.badges)}</div>'
        f'<p>{escape(body)}</p>'
        f'<div class="pcv2-panel-actions">{_actions(panel.actions)}</div>'
        f'</{tag}>'
    )


def _render_media(value: V2MediaItem | Mapping[str, Any], privacy: V2PrivacyContext) -> str:
    item = _coerce(value, V2MediaItem)
    if item.private and not privacy.is_owner:
        return ""
    src = item.poster_src or item.src
    tag = "a" if item.href else "article"
    href = _attr("href", item.href)
    classes = f"pcv2-media-tile pcv2-tone-{_tone(item.tone)}"
    if item.nsfw:
        classes += " is-blurred"
    if item.private:
        classes += " is-private"
    label = "Owner only" if item.private else item.kind
    return (
        f'<{tag} class="{classes}"{href}>'
        f'<img src="{escape(src)}" alt="{escape(item.title)}" loading="lazy">'
        '<span class="pcv2-media-copy">'
        f'<strong>{escape(item.title)}</strong>'
        f'<em>{escape(item.caption)}</em>'
        f'<span>{escape(label)}</span>{_badges(item.badges)}'
        '</span>'
        f'</{tag}>'
    )


def _render_table(section: V2Section, privacy: V2PrivacyContext) -> str:
    columns = _coerce_seq(section.columns, V2TableColumn)
    rows = _coerce_seq(section.rows, V2TableRow)
    if not columns:
        keys: list[str] = []
        for row in rows:
            for key in row.cells:
                if key not in keys:
                    keys.append(key)
        columns = tuple(V2TableColumn(key=key, label=key.replace("_", " ").title()) for key in keys)
    head = "".join(f"<th>{escape(column.label)}</th>" for column in columns)
    body: list[str] = []
    for row in rows:
        private_text = render_v2_private_text(row.private, privacy) if row.private else ""
        if row.private and not private_text:
            continue
        cells = []
        for column in columns:
            raw = private_text if row.private and column == columns[0] else row.cells.get(column.key, "")
            cells.append(f"<td>{escape(str(raw or ''))}</td>")
        tag = "a" if row.href else "tr"
        href = _attr("href", row.href)
        if tag == "a":
            body.append(
                f'<tr class="pcv2-table-link-row pcv2-tone-{_tone(row.tone)}">'
                f'<td colspan="{len(columns)}"><a{href}>{escape(str(row.cells.get(columns[0].key, row.title) or row.title))}</a>'
                f'{_badges(row.badges)}</td></tr>'
            )
        else:
            body.append(f'<tr class="pcv2-tone-{_tone(row.tone)}">{"".join(cells)}</tr>')
    if not body:
        body.append(f'<tr><td colspan="{max(1, len(columns))}">{escape(section.empty_text)}</td></tr>')
    return f'<div class="pcv2-table-wrap"><table class="pcv2-table"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def _render_messages(section: V2Section, privacy: V2PrivacyContext) -> str:
    messages = _coerce_seq(section.messages, V2ConversationMessage)
    if not messages:
        return f'<p class="pcv2-empty">{escape(section.empty_text)}</p>'
    out: list[str] = []
    for message in messages:
        body = render_v2_private_text(message.private, privacy) if message.private else message.body
        if message.private and not body:
            continue
        side = "right" if str(message.side).lower() == "right" else "left"
        avatar = (
            f'<img src="{escape(message.avatar_url)}" alt="" loading="lazy">'
            if message.avatar_url
            else f"<span>{escape(_initials(message.author))}</span>"
        )
        attachments = "".join(
            f'<a class="pcv2-message-attachment" href="{escape(str(item.get("href") or "#"))}">'
            f'{escape(str(item.get("label") or item.get("kind") or "attachment"))}</a>'
            for item in message.attachments
        )
        transcript = f'<details><summary>Transcript</summary><p>{escape(message.transcript)}</p></details>' if message.transcript else ""
        out.append(
            f'<article class="pcv2-message is-{side}">'
            f'<div class="pcv2-message-avatar">{avatar}</div>'
            '<div class="pcv2-message-bubble">'
            f'<div><strong>{escape(message.author)}</strong><span>{escape(message.when)}</span></div>'
            f'<p>{escape(body)}</p>{attachments}{transcript}'
            '</div></article>'
        )
    return '<div class="pcv2-thread" data-pcv2-scroll-bottom>' + "".join(out) + "</div>"


def render_v2_section(section: V2Section | Mapping[str, Any], privacy: V2PrivacyContext | Mapping[str, Any] | None = None) -> str:
    model = _coerce(section, V2Section)
    context = _coerce(privacy, V2PrivacyContext)
    layout = str(model.layout or "cards").strip().lower().replace("_", "-")
    search = ""
    if model.search_placeholder:
        search = (
            '<label class="pcv2-search">'
            f'<span>Search</span><input type="search" placeholder="{escape(model.search_placeholder, quote=True)}" data-pcv2-filter>'
            '</label>'
        )
    header = (
        f'<header class="pcv2-section-head"><div><h2>{escape(model.title)}</h2>'
        f'<p>{escape(model.subtitle)}</p></div><div>{_badges(model.badges)}{_actions(model.actions)}</div></header>{search}'
    )
    body = ""
    if layout in {"cards", "dashboard", "mind"}:
        cards = "".join(_render_card(card, context) for card in model.cards)
        panels = "".join(_render_panel(panel, context) for panel in model.panels)
        feed = "".join(_render_feed_item(item, context) for item in model.feed)
        if cards:
            body += f'<div class="pcv2-card-grid">{cards}</div>'
        if panels:
            body += f'<div class="pcv2-panel-grid">{panels}</div>'
        if feed:
            body += f'<div class="pcv2-feed">{feed}</div>'
    elif layout in {"feed", "timeline", "glossary"}:
        body = '<div class="pcv2-feed">' + "".join(_render_feed_item(item, context) for item in model.feed) + "</div>"
    elif layout in {"directory", "table", "people"}:
        body = _render_table(model, context)
    elif layout in {"conversation", "thread", "chat"}:
        panels = "".join(_render_panel(panel, context) for panel in model.panels)
        body = f'<div class="pcv2-conversation-shell"><aside>{panels}</aside>{_render_messages(model, context)}</div>'
    elif layout in {"media", "media-grid"}:
        body = '<div class="pcv2-media-grid">' + "".join(_render_media(item, context) for item in model.media) + "</div>"
    elif layout in {"journal", "diary"}:
        body = '<div class="pcv2-journal">' + "".join(_render_panel(panel, context) for panel in model.panels) + "</div>"
    elif layout in {"persona", "profile"}:
        body = '<div class="pcv2-profile-layout">' + "".join(_render_panel(panel, context) for panel in model.panels) + "</div>"
    elif layout in {"integrations", "control"}:
        body = '<div class="pcv2-panel-grid">' + "".join(_render_panel(panel, context) for panel in model.panels) + "</div>"
    else:
        body = '<div class="pcv2-panel-grid">' + "".join(_render_panel(panel, context) for panel in model.panels) + "</div>"
    if not body or body in {
        '<div class="pcv2-feed"></div>',
        '<div class="pcv2-media-grid"></div>',
        '<div class="pcv2-panel-grid"></div>',
    }:
        body = f'<p class="pcv2-empty">{escape(model.empty_text)}</p>'
    return f'<section id="{escape(_safe_id(model.key, "section"))}" class="pcv2-section pcv2-layout-{escape(layout)}">{header}{body}</section>'


def _render_hero(config: V2ConsoleConfig) -> str:
    hero = _hero(config)
    if hero.kind == "video":
        media = (
            f'<video class="pcv2-hero-media" poster="{escape(hero.poster_src or hero.mobile_src)}"'
            f'{_attr("autoplay", hero.autoplay, boolean=True)}{_attr("muted", hero.muted, boolean=True)}'
            f'{_attr("loop", hero.loop, boolean=True)}{_attr("controls", hero.controls, boolean=True)} playsinline>'
            f'<source src="{escape(hero.src)}"></video>'
        )
    else:
        media = (
            f'<picture><source media="(max-width: 720px)" srcset="{escape(hero.mobile_src or hero.src)}">'
            f'<img class="pcv2-hero-media" src="{escape(hero.src)}" alt="{escape(hero.alt_text)}"></picture>'
        )
    return (
        '<section class="pcv2-hero">'
        f'{media}<div class="pcv2-hero-copy"><span>{escape(config.page_subtitle)}</span>'
        f'<h1>{escape(config.page_title or config.brand_name)}</h1></div></section>'
    )


def _render_nav(config: V2ConsoleConfig) -> str:
    active = config.active_section
    items = _coerce_seq(config.nav_items, V2NavItem)
    links = []
    for item in items:
        if not item.enabled:
            continue
        cls = "pcv2-nav-item is-active" if item.key == active else "pcv2-nav-item"
        target = ' target="_blank" rel="noopener noreferrer"' if item.external else ""
        badge = f'<span class="pcv2-nav-badge">{escape(str(item.badge))}</span>' if item.badge not in (None, "", 0) else ""
        icon = f'<span aria-hidden="true">{escape(item.icon)}</span>' if item.icon else ""
        links.append(
            f'<a class="{cls}" href="{escape(item.href)}"{target}{_attr("title", item.title)}>'
            f'{icon}<strong>{escape(item.label)}</strong>{badge}</a>'
        )
    return '<nav class="pcv2-nav" aria-label="Console sections">' + "".join(links) + "</nav>"


def _render_operator(config: V2ConsoleConfig) -> str:
    operator = _operator(config)
    role = str(operator.role or "operator").replace("_", " ").title()
    initials = operator.initials or _initials(operator.display_name or operator.username)
    avatar = (
        f'<img src="{escape(operator.avatar_url)}" alt="">'
        if operator.avatar_url
        else f"<span>{escape(initials)}</span>"
    )
    read_only = " · read-only" if operator.read_only else ""
    return (
        '<div class="pcv2-operator">'
        f'<div class="pcv2-operator-avatar">{avatar}</div>'
        '<div><span>Signed in</span>'
        f'<strong>{escape(operator.display_name or operator.username or "Operator")}</strong>'
        f'<em>{escape(role + read_only)}</em></div></div>'
    )


def render_v2_console_page(config: V2ConsoleConfig | Mapping[str, Any]) -> str:
    model = _coerce(config, V2ConsoleConfig)
    theme = _theme(model)
    privacy = _privacy(model)
    sections = _coerce_seq(model.sections, V2Section)
    body = "".join(render_v2_section(section, privacy) for section in sections)
    live = ""
    if model.live_url:
        interval = max(1, int(model.live_interval_seconds or 15))
        live = (
            f'<span class="pcv2-live" data-pcv2-live-url="{escape(model.live_url, quote=True)}" '
            f'data-pcv2-live-interval="{interval}"><i></i>Live</span>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(model.page_title)} · {escape(model.brand_name)}</title>
  <style>
:root {{
{theme.css_variables()}
}}
  </style>
  <link rel="stylesheet" href="{escape(model.static_base_url.rstrip('/'))}/persona-console-v2.css">
  {model.extra_head}
</head>
<body class="pcv2-body" data-pcv2-active="{escape(model.active_section)}" data-pcv2-role="{escape(privacy.normalized_role)}">
  <header class="pcv2-topbar">
    <a class="pcv2-brand" href="{escape(model.home_href)}">{escape(model.brand_name)}</a>
    {_render_nav(model)}
    <div class="pcv2-status">{_badges(model.status_badges)}{live}{_render_operator(model)}</div>
  </header>
  <main class="pcv2-main">
    {_render_hero(model)}
    <div class="pcv2-content">{body}</div>
  </main>
  {model.footer_html}
  <script src="{escape(model.static_base_url.rstrip('/'))}/persona-console-v2.js"></script>
  {model.extra_body_end}
</body>
</html>"""
