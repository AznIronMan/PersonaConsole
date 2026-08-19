from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


V2_SECTION_KEYS: tuple[str, ...] = (
    "today",
    "conversations",
    "people",
    "mind",
    "journal",
    "memory",
    "media",
    "persona",
    "integrations",
    "control",
)


@dataclass(frozen=True)
class V2ThemeTokens:
    """Theme tokens for the v2 app-like console shell."""

    name: str = "default"
    background: str = "#06111f"
    background_alt: str = "#0a1b2f"
    surface: str = "#0c2237"
    surface_raised: str = "#102b44"
    surface_soft: str = "#123655"
    border: str = "#25516e"
    border_soft: str = "#17364f"
    text: str = "#f5fbff"
    text_muted: str = "#9bb7c9"
    text_soft: str = "#c9e5f4"
    accent: str = "#26d9ff"
    accent_2: str = "#2f80ff"
    accent_3: str = "#a7f3ff"
    success: str = "#34d399"
    warning: str = "#fbbf24"
    danger: str = "#fb7185"
    info: str = "#60a5fa"
    owner: str = "#f472b6"
    operator: str = "#22d3ee"
    moderator: str = "#a3a3a3"
    display_font_stack: str = (
        'Orbitron, "Rajdhani", "Arial Narrow", ui-sans-serif, system-ui, sans-serif'
    )
    body_font_stack: str = (
        'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, '
        '"Segoe UI", sans-serif'
    )
    mono_font_stack: str = (
        '"SFMono-Regular", Consolas, "Liberation Mono", ui-monospace, monospace'
    )
    radius: str = "8px"
    hero_min_height: str = "180px"

    def css_variables(self) -> str:
        values = {
            "--pcv2-bg": self.background,
            "--pcv2-bg-alt": self.background_alt,
            "--pcv2-surface": self.surface,
            "--pcv2-surface-raised": self.surface_raised,
            "--pcv2-surface-soft": self.surface_soft,
            "--pcv2-border": self.border,
            "--pcv2-border-soft": self.border_soft,
            "--pcv2-text": self.text,
            "--pcv2-text-muted": self.text_muted,
            "--pcv2-text-soft": self.text_soft,
            "--pcv2-accent": self.accent,
            "--pcv2-accent-2": self.accent_2,
            "--pcv2-accent-3": self.accent_3,
            "--pcv2-success": self.success,
            "--pcv2-warning": self.warning,
            "--pcv2-danger": self.danger,
            "--pcv2-info": self.info,
            "--pcv2-owner": self.owner,
            "--pcv2-operator": self.operator,
            "--pcv2-moderator": self.moderator,
            "--pcv2-display-font": self.display_font_stack,
            "--pcv2-body-font": self.body_font_stack,
            "--pcv2-mono-font": self.mono_font_stack,
            "--pcv2-radius": self.radius,
            "--pcv2-hero-min-height": self.hero_min_height,
        }
        return "\n".join(f"  {name}: {value};" for name, value in values.items())


@dataclass(frozen=True)
class V2HeroMedia:
    kind: str = "image"
    src: str = "/persona-console/static/placeholders/hero-desktop-missing.svg"
    mobile_src: str = "/persona-console/static/placeholders/hero-mobile-missing.svg"
    poster_src: str = ""
    alt_text: str = "Console hero media"
    autoplay: bool = True
    muted: bool = True
    loop: bool = True
    controls: bool = False
    focus_x: str = "50%"
    focus_y: str = "50%"


@dataclass(frozen=True)
class V2NavItem:
    key: str
    label: str
    href: str
    icon: str = ""
    enabled: bool = True
    badge: int | str | None = None
    feature: str = ""
    title: str = ""
    external: bool = False


@dataclass(frozen=True)
class V2OperatorContext:
    display_name: str = "Operator"
    username: str = ""
    role: str = "operator"
    read_only: bool = False
    avatar_url: str = ""
    initials: str = ""


@dataclass(frozen=True)
class V2PrivacyContext:
    role: str = "operator"
    owner_role: str = "owner"
    can_view_owner_only: bool = False
    read_only: bool = False

    @property
    def normalized_role(self) -> str:
        return str(self.role or "operator").strip().lower().replace("-", "_").replace(" ", "_")

    @property
    def is_owner(self) -> bool:
        return self.can_view_owner_only or self.normalized_role == self.owner_role


@dataclass(frozen=True)
class V2PrivateValue:
    text: str = ""
    safe_alternate: str = ""
    owner_only: bool = False
    lockable: bool = True
    locked: bool = False
    hide_without_alternate: bool = False


@dataclass(frozen=True)
class V2Badge:
    label: str
    tone: str = "neutral"
    title: str = ""
    icon_src: str = ""


@dataclass(frozen=True)
class V2Action:
    label: str
    href: str = "#"
    icon: str = ""
    tone: str = "neutral"
    method: str = "get"
    title: str = ""
    disabled: bool = False


@dataclass(frozen=True)
class V2MetricCard:
    label: str
    value: str = ""
    detail: str = ""
    tone: str = "neutral"
    href: str = ""
    icon: str = ""
    icon_src: str = ""
    title: str = ""
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    meta: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2FeedItem:
    title: str
    detail: str = ""
    when: str = ""
    href: str = ""
    icon: str = ""
    icon_src: str = ""
    provider: str = ""
    tone: str = "neutral"
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    media: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2RecentExchange:
    user_common_name: str = ""
    message: str = ""
    full_message: str = ""
    platform_label: str = ""
    platform: str = ""
    platform_icon_src: str = ""
    direction: str = ""
    persona_common_name: str = ""
    persona_avatar_url: str = ""
    persona_initials: str = ""
    avatar_url: str = ""
    initials: str = ""
    relative_time: str = ""
    timestamp: str = ""
    href: str = ""
    tone: str = "neutral"
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    media: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2TableColumn:
    key: str
    label: str
    width: str = ""


@dataclass(frozen=True)
class V2TableRow:
    cells: Mapping[str, Any]
    href: str = ""
    title: str = ""
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    actions: Sequence[V2Action | Mapping[str, Any] | str] = field(default_factory=tuple)
    tone: str = "neutral"
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2MediaItem:
    title: str
    src: str = "/persona-console/static/placeholders/media-tile-missing.svg"
    href: str = ""
    kind: str = "image"
    poster_src: str = ""
    caption: str = ""
    tone: str = "neutral"
    nsfw: bool = False
    private: bool = False
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    actions: Sequence[V2Action | Mapping[str, Any] | str] = field(default_factory=tuple)
    meta: Sequence[Mapping[str, Any]] = field(default_factory=tuple)


@dataclass(frozen=True)
class V2ConversationMessage:
    author: str
    body: str = ""
    side: str = "left"
    when: str = ""
    avatar_url: str = ""
    provider: str = ""
    attachments: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    transcript: str = ""
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2Panel:
    title: str
    body: str = ""
    href: str = ""
    tone: str = "neutral"
    icon: str = ""
    actions: Sequence[V2Action | Mapping[str, Any] | str] = field(default_factory=tuple)
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    private: V2PrivateValue | Mapping[str, Any] | str | None = None


@dataclass(frozen=True)
class V2Section:
    key: str
    title: str
    subtitle: str = ""
    layout: str = "cards"
    href: str = ""
    actions: Sequence[V2Action | Mapping[str, Any] | str] = field(default_factory=tuple)
    badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    cards: Sequence[V2MetricCard | Mapping[str, Any]] = field(default_factory=tuple)
    feed: Sequence[V2FeedItem | Mapping[str, Any]] = field(default_factory=tuple)
    exchanges: Sequence[V2RecentExchange | Mapping[str, Any]] = field(default_factory=tuple)
    panels: Sequence[V2Panel | Mapping[str, Any]] = field(default_factory=tuple)
    media: Sequence[V2MediaItem | Mapping[str, Any]] = field(default_factory=tuple)
    messages: Sequence[V2ConversationMessage | Mapping[str, Any]] = field(default_factory=tuple)
    columns: Sequence[V2TableColumn | Mapping[str, Any]] = field(default_factory=tuple)
    rows: Sequence[V2TableRow | Mapping[str, Any]] = field(default_factory=tuple)
    empty_text: str = "Nothing to show yet."
    search_placeholder: str = ""
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class V2ConsoleConfig:
    brand_name: str = "Persona"
    page_title: str = "Console"
    page_subtitle: str = ""
    active_section: str = "today"
    home_href: str = "/"
    static_base_url: str = "/persona-console/static"
    static_version: str = ""
    theme: V2ThemeTokens | Mapping[str, Any] | None = None
    hero: V2HeroMedia | Mapping[str, Any] | None = None
    nav_items: Sequence[V2NavItem | Mapping[str, Any]] = field(default_factory=tuple)
    operator: V2OperatorContext | Mapping[str, Any] | None = None
    privacy: V2PrivacyContext | Mapping[str, Any] | None = None
    sections: Sequence[V2Section | Mapping[str, Any]] = field(default_factory=tuple)
    status_badges: Sequence[V2Badge | Mapping[str, Any] | str] = field(default_factory=tuple)
    extra_head: str = ""
    extra_body_end: str = ""
    live_url: str = ""
    live_interval_seconds: int = 0
    footer_html: str = ""
