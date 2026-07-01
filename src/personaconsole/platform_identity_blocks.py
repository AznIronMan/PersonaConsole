from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
from html import escape
from typing import Any, Mapping, Sequence, TypeVar

from .controls import render_status_tabs
from .dashboard import render_dashboard_filters, render_dashboard_metrics
from .models import (
    PlatformIdentityBlockRow,
    PlatformIdentityBlocksSurfaceConfig,
    SurfaceAction,
    SurfaceBadge,
)
from .privacy import (
    WITHHELD_PRIVATE_TEXT,
    AdminPrivacyContext,
    OwnerPrivateScopePolicy,
    PrivacyRenderMode,
    can_view_raw_private,
    feature_enabled,
    privacy_render_mode,
    render_private_text,
)
from .render import render_live_controls

PLATFORM_IDENTITY_BLOCKS_FEATURE = "platform_identity_blocks"

T = TypeVar("T")

_TONE_ALIASES = {
    "active": "good",
    "allow": "good",
    "allowed": "good",
    "applied": "good",
    "bad": "bad",
    "blocked": "bad",
    "danger": "bad",
    "denied": "bad",
    "disabled": "neutral",
    "failed": "bad",
    "good": "good",
    "healthy": "good",
    "info": "info",
    "missing": "warn",
    "not_applicable": "neutral",
    "not applicable": "neutral",
    "not_requested": "neutral",
    "not requested": "neutral",
    "ok": "good",
    "pending": "warn",
    "queued": "warn",
    "ready": "good",
    "review": "warn",
    "suppressed": "bad",
    "unknown": "neutral",
    "warn": "warn",
    "warning": "warn",
    "": "neutral",
}


def _mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _coerce(value: T | Mapping[str, object], cls: type[T], defaults: Mapping[str, Any] | None = None) -> T:
    if isinstance(value, cls):
        return value
    data = {**(defaults or {}), **_mapping(value)}
    allowed = {field.name for field in fields(cls)}
    return cls(**{key: value for key, value in data.items() if key in allowed})


def _tone(value: object) -> str:
    return _TONE_ALIASES.get(str(value or "").strip().lower().replace("-", "_"), "neutral")


def _key(value: object, default: str = "identity") -> str:
    raw = str(value or default or "").strip().lower().replace("_", "-")
    safe = "".join(char for char in raw if char.isalnum() or char == "-")
    return safe or default


def _label(value: object) -> str:
    text = str(value or "").strip().replace("_", " ").replace("-", " ")
    return " ".join(part.capitalize() for part in text.split()) if text else ""


def _attrs(**attrs: object) -> str:
    parts: list[str] = []
    for name, value in attrs.items():
        if value not in (None, False, ""):
            parts.append(f' {name.replace("_", "-")}="{escape(str(value), quote=True)}"')
    return "".join(parts)


def _private_text(
    text: object,
    *,
    privacy_scope: str,
    safe_alternate: str,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    if not privacy_scope:
        return str(text or "")
    if policy is None:
        return str(safe_alternate or "").strip() or WITHHELD_PRIVATE_TEXT
    return render_private_text(
        str(text or ""),
        safe_alternate=safe_alternate,
        policy=policy,
        context=context,
        scope=privacy_scope,
    )


def _raw_href(
    href: str,
    *,
    privacy_scope: str,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    if not href or not privacy_scope:
        return href
    if policy is None:
        return ""
    if not policy.is_owner_private_scope(privacy_scope):
        return href
    return href if can_view_raw_private(policy, context, privacy_scope) else ""


def _is_private(
    *,
    privacy_scope: str,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> bool:
    if not privacy_scope:
        return False
    if policy is None:
        return True
    mode = privacy_render_mode(
        policy,
        context,
        privacy_scope,
        has_safe_alternate=False,
        hide_without_safe_alternate=True,
    )
    return mode != PrivacyRenderMode.RAW


def _badge_html(raw_badge: SurfaceBadge | Mapping[str, object] | str) -> str:
    badge = SurfaceBadge(str(raw_badge)) if isinstance(raw_badge, str) else _coerce(raw_badge, SurfaceBadge)
    if not badge.label:
        return ""
    return f'<span class="pc-platform-block-badge pc-dashboard-tone-{_tone(badge.tone)}">{escape(str(badge.label))}</span>'


def _badges_html(badges: Sequence[SurfaceBadge | Mapping[str, object] | str]) -> str:
    body = "".join(_badge_html(badge) for badge in badges)
    return f'<div class="pc-platform-block-badges">{body}</div>' if body else ""


def _action_html(raw_action: SurfaceAction | Mapping[str, object], features: Mapping[str, bool] | None) -> str:
    action = _coerce(raw_action, SurfaceAction)
    if not action.label or (action.feature and not feature_enabled(features, action.feature, default=True)):
        return ""
    method = str(action.method or "").strip().upper()
    cls = f"pc-platform-block-action pc-dashboard-tone-{_tone(action.tone)}"
    body = escape(str(action.label))
    if action.disabled or not action.href:
        disabled = ' aria-disabled="true"' if action.disabled else ""
        return f'<span class="{cls} is-disabled"{_attrs(title=action.title)}{disabled}>{body}</span>'
    return f'<a class="{cls}" href="{escape(str(action.href), quote=True)}"{_attrs(data_method=method) if method else ""}{_attrs(title=action.title)}>{body}</a>'


def _actions_html(actions: Sequence[SurfaceAction | Mapping[str, object]], features: Mapping[str, bool] | None) -> str:
    body = "".join(_action_html(action, features) for action in actions)
    return f'<div class="pc-platform-block-actions">{body}</div>' if body else ""


def _status_html(label: str, status: object, tone: object = "", reason: object = "", updated: object = "") -> str:
    status_text = str(status or "unknown")
    meta = " ".join(part for part in (str(reason or ""), str(updated or "")) if part)
    return (
        '<div class="pc-platform-block-state">'
        f'<span>{escape(label)}</span>'
        f'<strong class="pc-dashboard-tone-{_tone(tone or status_text)}">{escape(_label(status_text) or "Unknown")}</strong>'
        + (f"<small>{escape(meta)}</small>" if meta else "")
        + "</div>"
    )


def _facts_html(row: PlatformIdentityBlockRow) -> str:
    pairs = (
        ("Platform", row.platform),
        ("Person", row.person_label or row.person_key),
        ("Trust", row.trust_label),
        ("Posture", row.posture_label),
        ("Provider", row.provider_label),
        ("Job", row.job_label),
        ("Age", row.updated_age),
    )
    parts = [
        f'<span><b>{escape(label)}</b>{escape(str(value))}</span>'
        for label, value in pairs
        if value not in ("", None)
    ]
    return f'<div class="pc-platform-block-facts">{"".join(parts)}</div>' if parts else ""


def _row_label(
    row: PlatformIdentityBlockRow,
    *,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    if not row.privacy_scope:
        return str(row.label or row.key)
    if _is_private(privacy_scope=row.privacy_scope, policy=policy, context=context):
        return str(row.safe_label or row.safe_alternate or WITHHELD_PRIVATE_TEXT)
    return str(row.label or row.key)


def _row_html(
    row: PlatformIdentityBlockRow,
    *,
    features: Mapping[str, bool] | None,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    private = _is_private(privacy_scope=row.privacy_scope, policy=policy, context=context)
    label = _row_label(row, policy=policy, context=context)
    href = _raw_href(row.href, privacy_scope=row.privacy_scope, policy=policy, context=context)
    internal_reason = _private_text(row.internal_reason, privacy_scope=row.privacy_scope, safe_alternate="", policy=policy, context=context)
    platform_reason = _private_text(row.platform_reason, privacy_scope=row.privacy_scope, safe_alternate="", policy=policy, context=context)
    summary = _private_text(row.summary, privacy_scope=row.privacy_scope, safe_alternate=row.safe_alternate, policy=policy, context=context)
    cls = f"pc-platform-block-row pc-dashboard-tone-{_tone(row.internal_block_tone or row.internal_block_state)}"
    if private:
        cls += " is-private"
    body = (
        '<div class="pc-platform-block-main">'
        '<div class="pc-platform-block-title">'
        f'<strong>{escape(label)}</strong>'
        f'<span>{escape(str(row.platform or "platform"))}</span>'
        "</div>"
        + ("" if private else _facts_html(row))
        + (f"<p>{escape(summary)}</p>" if summary else "")
        + _badges_html(row.badges)
        + "</div>"
        '<div class="pc-platform-block-state-grid">'
        + _status_html("Internal", row.internal_block_state, row.internal_block_tone, internal_reason, row.internal_updated)
        + _status_html("Platform", row.platform_block_status, row.platform_block_tone, platform_reason, row.platform_updated)
        + "</div>"
        + _actions_html(row.actions, features)
    )
    if href and not row.actions:
        return f'<a class="{cls}" href="{escape(href, quote=True)}" data-platform-identity-block="{escape(_key(row.key), quote=True)}">{body}</a>'
    return f'<article class="{cls}" data-platform-identity-block="{escape(_key(row.key), quote=True)}">{body}</article>'


def _sort_value(row: PlatformIdentityBlockRow, key: str) -> str:
    clean = key.strip().lower().replace("-", "_")
    value = {
        "platform": row.platform,
        "label": row.label,
        "identity": row.label,
        "person": row.person_label or row.person_key,
        "person_label": row.person_label,
        "trust": row.trust_label,
        "posture": row.posture_label,
        "internal": row.internal_block_state,
        "internal_block_state": row.internal_block_state,
        "platform_block": row.platform_block_status,
        "platform_block_status": row.platform_block_status,
        "provider": row.provider_label,
        "updated": row.updated_age or row.internal_updated or row.platform_updated,
        "age": row.updated_age,
    }.get(clean, "")
    return str(value or "").lower()


def _sorted_rows(rows: Sequence[PlatformIdentityBlockRow], *, sort_key: str, direction: str) -> tuple[PlatformIdentityBlockRow, ...]:
    if not sort_key:
        return tuple(rows)
    reverse = str(direction or "").strip().lower() == "desc"
    return tuple(sorted(rows, key=lambda row: (_sort_value(row, sort_key), str(row.key)), reverse=reverse))


def platform_identity_blocks_feature_enabled(
    config: PlatformIdentityBlocksSurfaceConfig | Mapping[str, object],
    features: Mapping[str, bool] | None = None,
) -> bool:
    model = _coerce(config, PlatformIdentityBlocksSurfaceConfig)
    return bool(model.enabled) and feature_enabled(features, str(model.feature or PLATFORM_IDENTITY_BLOCKS_FEATURE), default=True)


def render_platform_identity_blocks_surface(
    config: PlatformIdentityBlocksSurfaceConfig | Mapping[str, object] | None,
    *,
    features: Mapping[str, bool] | None = None,
    privacy_policy: OwnerPrivateScopePolicy | None = None,
    privacy_context: AdminPrivacyContext | Mapping[str, Any] | None = None,
) -> str:
    if config is None:
        return ""
    model = _coerce(config, PlatformIdentityBlocksSurfaceConfig)
    if not platform_identity_blocks_feature_enabled(model, features):
        return ""
    rows = tuple(_coerce(row, PlatformIdentityBlockRow, {"key": "identity", "label": "Identity"}) for row in model.rows)
    rows = _sorted_rows(rows, sort_key=model.sort_key, direction=model.sort_direction)
    tabs = render_status_tabs(model.tabs, aria_label=f"{model.title} status") if model.tabs else ""
    filters = render_dashboard_filters(model.filters) if model.filters else ""
    metrics = render_dashboard_metrics(model.metrics) if model.metrics else ""
    live = render_live_controls(model.live_refresh) if model.live_refresh else ""
    actions = _actions_html(model.actions, features)
    sort = ""
    if model.sort_key:
        direction = "descending" if str(model.sort_direction or "").strip().lower() == "desc" else "ascending"
        label = model.sort_label or _label(model.sort_key)
        sort = f'<div class="pc-platform-block-sort">Sorted by {escape(str(label))} ({direction})</div>'
    row_html = "".join(
        _row_html(row, features=features, policy=privacy_policy, context=privacy_context)
        for row in rows
    )
    if not row_html:
        row_html = f'<div class="pc-dashboard-empty">{escape(str(model.empty_label))}</div>'
    status = f'<span class="pc-surface-status pc-dashboard-tone-{_tone(model.status_tone or model.status)}">{escape(str(model.status))}</span>' if model.status else ""
    return (
        f'<section id="{escape(_key(model.key, "platform-identity-blocks"), quote=True)}" class="pc-platform-block-surface pc-dashboard-surface">'
        '<div class="pc-dashboard-overview-head"><div>'
        f'<div class="pc-dashboard-section-title">{escape(str(model.title))}</div>'
        f'<div class="pc-dashboard-section-meta">{escape(str(model.subtitle))}</div>'
        f"</div>{status}</div>"
        f"{tabs}{filters}{metrics}{live}{actions}{sort}"
        f'<div class="pc-platform-block-list">{row_html}</div>'
        "</section>"
    )


__all__ = [
    "PLATFORM_IDENTITY_BLOCKS_FEATURE",
    "platform_identity_blocks_feature_enabled",
    "render_platform_identity_blocks_surface",
]
