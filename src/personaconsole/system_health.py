from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
from html import escape
from typing import Any, Mapping, Sequence, TypeVar

from .controls import render_status_tabs
from .models import (
    DashboardMetric,
    StatusTab,
    SurfaceAction,
    SurfaceBadge,
    SystemAuditRow,
    SystemDatabaseCard,
    SystemHealthCheck,
    SystemHealthGroup,
    SystemHealthSurfaceConfig,
    SystemReadinessProbe,
    SystemSecretCoverageRow,
    SystemTableSummary,
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

SYSTEM_HEALTH_FEATURE = "system_health"

T = TypeVar("T")

_TONE_ALIASES = {
    "bad": "bad",
    "blocked": "bad",
    "critical": "bad",
    "danger": "bad",
    "down": "bad",
    "error": "bad",
    "failed": "bad",
    "missing": "bad",
    "unhealthy": "bad",
    "warn": "warn",
    "warning": "warn",
    "degraded": "warn",
    "held": "warn",
    "lagging": "warn",
    "pending": "warn",
    "stale": "warn",
    "unknown": "neutral",
    "good": "good",
    "healthy": "good",
    "ok": "good",
    "ready": "good",
    "success": "good",
    "info": "info",
    "notice": "info",
    "neutral": "neutral",
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
    data = {key: value for key, value in data.items() if key in allowed}
    return cls(**data)


def _tone(value: object) -> str:
    return _TONE_ALIASES.get(str(value or "").strip().lower(), "neutral")


def _key(value: object, default: str = "item") -> str:
    raw = str(value or default or "").strip().lower().replace("_", "-")
    safe = "".join(char for char in raw if char.isalnum() or char == "-")
    return safe or default


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


def _private_class(
    *,
    privacy_scope: str,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    if not privacy_scope:
        return ""
    if policy is None:
        return " is-private"
    mode = privacy_render_mode(
        policy,
        context,
        privacy_scope,
        has_safe_alternate=False,
        hide_without_safe_alternate=True,
    )
    return " is-private" if mode != PrivacyRenderMode.RAW else ""


def _badge_html(raw_badge: SurfaceBadge | Mapping[str, object] | str) -> str:
    badge = SurfaceBadge(str(raw_badge)) if isinstance(raw_badge, str) else _coerce(raw_badge, SurfaceBadge)
    if not badge.label:
        return ""
    return f'<span class="pc-system-badge pc-dashboard-tone-{_tone(badge.tone)}">{escape(str(badge.label))}</span>'


def _badges_html(badges: Sequence[SurfaceBadge | Mapping[str, object] | str]) -> str:
    body = "".join(_badge_html(badge) for badge in badges)
    return f'<div class="pc-system-badges">{body}</div>' if body else ""


def _action_html(raw_action: SurfaceAction | Mapping[str, object]) -> str:
    action = _coerce(raw_action, SurfaceAction)
    if not action.label:
        return ""
    cls = f"pc-system-action pc-dashboard-tone-{_tone(action.tone)}"
    body = escape(str(action.label))
    title = _attrs(title=action.title)
    method = str(action.method or "").strip().upper()
    if action.disabled or not action.href:
        disabled = ' aria-disabled="true"' if action.disabled else ""
        return f'<span class="{cls} is-disabled"{title}{disabled}>{body}</span>'
    return f'<a class="{cls}" href="{escape(action.href, quote=True)}"{_attrs(data_method=method) if method else ""}{title}>{body}</a>'


def _actions_html(actions: Sequence[SurfaceAction | Mapping[str, object]]) -> str:
    body = "".join(_action_html(action) for action in actions)
    return f'<div class="pc-system-actions">{body}</div>' if body else ""


def system_health_surface_feature_enabled(
    config: SystemHealthSurfaceConfig | Mapping[str, object],
    features: Mapping[str, bool] | None = None,
) -> bool:
    model = _coerce(config, SystemHealthSurfaceConfig)
    return bool(model.enabled) and feature_enabled(features, str(model.feature or SYSTEM_HEALTH_FEATURE), default=True)


def _metric_html(raw_metric: DashboardMetric | Mapping[str, object]) -> str:
    metric = _coerce(raw_metric, DashboardMetric, {"label": "Metric", "value": ""})
    body = (
        f'<span class="pc-system-metric-label">{escape(str(metric.label))}</span>'
        f'<strong>{escape(str(metric.value))}</strong>'
        f'<small>{escape(str(metric.detail))}</small>'
    )
    cls = f"pc-system-metric pc-dashboard-tone-{_tone(metric.tone)}"
    if metric.href:
        return f'<a class="{cls}" href="{escape(str(metric.href), quote=True)}">{body}</a>'
    return f'<article class="{cls}">{body}</article>'


def _metrics_html(metrics: Sequence[DashboardMetric | Mapping[str, object]]) -> str:
    body = "".join(_metric_html(metric) for metric in metrics)
    return f'<div class="pc-system-metrics">{body}</div>' if body else ""


def _check_html(raw_check: SystemHealthCheck | Mapping[str, object]) -> str:
    check = _coerce(raw_check, SystemHealthCheck, {"key": "check"})
    tone = _tone(check.tone or check.status)
    flags = "".join(
        part
        for part in [
            '<span class="pc-system-required">required</span>' if check.required else "",
            '<span class="pc-system-blocked">blocked</span>' if check.blocked else "",
            f'<time>{escape(str(check.updated))}</time>' if check.updated else "",
        ]
    )
    body = (
        '<div class="pc-system-row-main">'
        f'<div class="pc-system-row-title"><strong>{escape(str(check.label or check.key))}</strong>'
        f'<span class="pc-surface-status pc-dashboard-tone-{tone}">{escape(str(check.status or "unknown"))}</span></div>'
        f'<p>{escape(str(check.summary or check.detail))}</p>'
        f'<div class="pc-system-row-meta">{flags}{_badges_html(check.badges)}</div>'
        '</div>'
        f'<div class="pc-system-row-value">{escape(str(check.value))}</div>'
        f'{_actions_html(check.actions)}'
    )
    if check.href:
        return f'<a class="pc-system-row pc-system-check pc-dashboard-tone-{tone}" href="{escape(check.href, quote=True)}">{body}</a>'
    return f'<article class="pc-system-row pc-system-check pc-dashboard-tone-{tone}">{body}</article>'


def _health_group_html(raw_group: SystemHealthGroup | Mapping[str, object]) -> str:
    group = _coerce(raw_group, SystemHealthGroup, {"key": "health", "title": "Health"})
    checks = "".join(_check_html(check) for check in group.checks)
    if not checks:
        checks = '<div class="pc-dashboard-empty">No checks in this group.</div>'
    tone = _tone(group.tone or group.status)
    status = f'<span class="pc-surface-status pc-dashboard-tone-{tone}">{escape(str(group.status))}</span>' if group.status else ""
    return (
        f'<section class="pc-system-group pc-dashboard-panel pc-dashboard-tone-{tone}" data-system-group="{escape(_key(group.key), quote=True)}">'
        '<div class="pc-dashboard-panel-head"><div>'
        f'<div class="pc-dashboard-section-title">{escape(str(group.title))}</div>'
        f'<div class="pc-dashboard-section-meta">{escape(str(group.description))}</div>'
        f'</div><div class="pc-system-group-meta">{status}{_badges_html(group.badges)}{_actions_html(group.actions)}</div></div>'
        f'<div class="pc-system-list">{checks}</div></section>'
    )


def _database_card_html(raw_card: SystemDatabaseCard | Mapping[str, object]) -> str:
    card = _coerce(raw_card, SystemDatabaseCard, {"key": "database"})
    tone = _tone(card.tone or card.status)
    pairs = [
        ("Database", card.database),
        ("User", card.user),
        ("Host", card.host),
        ("Schema", card.schema_version),
        ("Tables", card.tables),
        ("Records", card.records),
        ("Latency", card.latency),
    ]
    details = "".join(f'<span><b>{escape(label)}</b>{escape(str(value))}</span>' for label, value in pairs if value != "")
    body = (
        '<div class="pc-system-card-head">'
        f'<strong>{escape(str(card.label))}</strong>'
        f'<span class="pc-surface-status pc-dashboard-tone-{tone}">{escape(str(card.status))}</span></div>'
        f'<p>{escape(str(card.summary))}</p>'
        f'<div class="pc-system-card-grid">{details}</div>{_badges_html(card.badges)}{_actions_html(card.actions)}'
    )
    cls = f"pc-system-card pc-system-database pc-dashboard-tone-{tone}"
    if card.href:
        return f'<a class="{cls}" href="{escape(card.href, quote=True)}">{body}</a>'
    return f'<article class="{cls}">{body}</article>'


def _database_cards_html(cards: Sequence[SystemDatabaseCard | Mapping[str, object]]) -> str:
    body = "".join(_database_card_html(card) for card in cards)
    return f'<section class="pc-system-section"><div class="pc-dashboard-section-title">Database</div><div class="pc-system-card-grid-wrap">{body}</div></section>' if body else ""


def _table_html(rows: Sequence[SystemTableSummary | Mapping[str, object]]) -> str:
    if not rows:
        return ""
    body = ""
    for raw_row in rows:
        row = _coerce(raw_row, SystemTableSummary, {"name": "table"})
        tone = _tone(row.tone or row.status)
        name = f'<a href="{escape(row.href, quote=True)}">{escape(str(row.name))}</a>' if row.href else escape(str(row.name))
        body += (
            f'<tr class="pc-dashboard-tone-{tone}"><td>{name}</td><td>{escape(str(row.status))}</td>'
            f'<td>{escape(str(row.schema))}</td><td>{escape(str(row.rows))}</td>'
            f'<td>{escape(str(row.owner))}</td><td>{escape(str(row.updated))}</td>'
            f'<td>{escape(str(row.detail))}{_badges_html(row.badges)}</td></tr>'
        )
    return (
        '<section class="pc-system-section"><div class="pc-dashboard-section-title">Schema And Tables</div>'
        '<div class="pc-system-table-wrap"><table class="pc-system-table">'
        '<thead><tr><th>Name</th><th>Status</th><th>Schema</th><th>Rows</th><th>Owner</th><th>Updated</th><th>Detail</th></tr></thead>'
        f'<tbody>{body}</tbody></table></div></section>'
    )


def _secret_html(rows: Sequence[SystemSecretCoverageRow | Mapping[str, object]]) -> str:
    if not rows:
        return ""
    cards = []
    for raw_row in rows:
        row = _coerce(raw_row, SystemSecretCoverageRow, {"key": "secret", "label": "Secret coverage"})
        tone = _tone(row.tone or row.status)
        metrics = "".join(
            f'<span><b>{label}</b>{escape(str(value))}</span>'
            for label, value in (("Present", row.present), ("Missing", row.missing), ("Required", row.required), ("Optional", row.optional))
            if value != ""
        )
        body = (
            '<div class="pc-system-card-head">'
            f'<strong>{escape(str(row.label))}</strong>'
            f'<span class="pc-surface-status pc-dashboard-tone-{tone}">{escape(str(row.status))}</span></div>'
            f'<p>{escape(str(row.summary))}</p><div class="pc-system-card-grid">{metrics}</div>{_badges_html(row.badges)}{_actions_html(row.actions)}'
        )
        cls = f"pc-system-card pc-system-secret pc-dashboard-tone-{tone}"
        cards.append(f'<a class="{cls}" href="{escape(row.href, quote=True)}">{body}</a>' if row.href else f'<article class="{cls}">{body}</article>')
    return f'<section class="pc-system-section"><div class="pc-dashboard-section-title">Secret Coverage</div><div class="pc-system-card-grid-wrap">{"".join(cards)}</div></section>'


def _readiness_html(rows: Sequence[SystemReadinessProbe | Mapping[str, object]]) -> str:
    if not rows:
        return ""
    body = ""
    for raw_row in rows:
        row = _coerce(raw_row, SystemReadinessProbe, {"key": "probe", "label": "Probe"})
        tone = _tone(row.tone or row.status)
        required = '<span class="pc-system-required">required</span>' if row.required else '<span>optional</span>'
        body += (
            f'<article class="pc-system-row pc-system-probe pc-dashboard-tone-{tone}">'
            '<div class="pc-system-row-main">'
            f'<div class="pc-system-row-title"><strong>{escape(str(row.label))}</strong><span class="pc-surface-status pc-dashboard-tone-{tone}">{escape(str(row.status))}</span></div>'
            f'<p>{escape(str(row.summary or row.detail))}</p><div class="pc-system-row-meta">{required}<time>{escape(str(row.checked_at))}</time>{_badges_html(row.badges)}</div></div>'
            f'{_actions_html(row.actions)}</article>'
        )
    return f'<section class="pc-system-section"><div class="pc-dashboard-section-title">Readiness</div><div class="pc-system-list">{body}</div></section>'


def _audit_html(
    rows: Sequence[SystemAuditRow | Mapping[str, object]],
    *,
    policy: OwnerPrivateScopePolicy | None,
    context: AdminPrivacyContext | Mapping[str, Any] | None,
) -> str:
    if not rows:
        return ""
    body = ""
    for raw_row in rows:
        row = _coerce(raw_row, SystemAuditRow, {"key": "audit", "label": "Audit"})
        tone = _tone(row.tone or row.status)
        summary = _private_text(row.summary or row.detail, privacy_scope=row.privacy_scope, safe_alternate=row.safe_alternate, policy=policy, context=context)
        href = _raw_href(row.href, privacy_scope=row.privacy_scope, policy=policy, context=context)
        private = _private_class(privacy_scope=row.privacy_scope, policy=policy, context=context)
        label = f'<a href="{escape(href, quote=True)}">{escape(str(row.label))}</a>' if href else escape(str(row.label))
        body += (
            f'<tr class="pc-dashboard-tone-{tone}{private}"><td>{label}</td><td>{escape(str(row.action))}</td>'
            f'<td>{escape(str(row.actor))}</td><td>{escape(str(row.status))}</td><td>{escape(str(row.timestamp))}</td>'
            f'<td>{escape(summary)}{_badges_html(row.badges)}{_actions_html(row.actions)}</td></tr>'
        )
    return (
        '<section class="pc-system-section"><div class="pc-dashboard-section-title">Audit Events</div>'
        '<div class="pc-system-table-wrap"><table class="pc-system-table">'
        '<thead><tr><th>Event</th><th>Action</th><th>Actor</th><th>Status</th><th>Time</th><th>Summary</th></tr></thead>'
        f'<tbody>{body}</tbody></table></div></section>'
    )


def render_system_health_surface(
    config: SystemHealthSurfaceConfig | Mapping[str, object] | None,
    *,
    features: Mapping[str, bool] | None = None,
    privacy_policy: OwnerPrivateScopePolicy | None = None,
    privacy_context: AdminPrivacyContext | Mapping[str, Any] | None = None,
) -> str:
    if config is None:
        return ""
    model = _coerce(config, SystemHealthSurfaceConfig)
    if not system_health_surface_feature_enabled(model, features):
        return ""
    tabs = render_status_tabs(tuple(_coerce(tab, StatusTab, {"label": "Tab"}) for tab in model.tabs), aria_label="System posture filters") if model.tabs else ""
    groups = "".join(_health_group_html(group) for group in model.health_groups)
    body = "".join(
        part
        for part in [
            tabs,
            _metrics_html(model.metrics),
            groups,
            _database_cards_html(model.databases),
            _table_html(model.tables),
            _secret_html(model.secret_coverage),
            _readiness_html(model.readiness),
            _audit_html(model.audit_rows, policy=privacy_policy, context=privacy_context),
        ]
    )
    if not body:
        body = f'<div class="pc-dashboard-empty">{escape(str(model.empty_label))}</div>'
    return (
        f'<section id="{escape(_key(model.key, "system-health"), quote=True)}" class="pc-system-health-surface pc-dashboard-surface">'
        '<div class="pc-dashboard-overview-head"><div>'
        f'<div class="pc-dashboard-section-title">{escape(str(model.title))}</div>'
        f'<div class="pc-dashboard-section-meta">{escape(str(model.subtitle))}</div>'
        f'</div>{_actions_html(model.actions)}</div>{body}</section>'
    )
