from personaconsole import (
    PLATFORM_IDENTITY_BLOCKS_FEATURE,
    AdminPrivacyContext,
    DashboardFilter,
    DashboardMetric,
    LiveRefreshConfig,
    OwnerPrivateScopePolicy,
    PlatformIdentityBlockRow,
    PlatformIdentityBlocksSurfaceConfig,
    StatusTab,
    SurfaceAction,
    platform_identity_blocks_feature_enabled,
    render_platform_identity_blocks_surface,
)


def _policy() -> OwnerPrivateScopePolicy:
    return OwnerPrivateScopePolicy(owner_private_scopes={"owner_private": ("owner",)})


def _operator() -> AdminPrivacyContext:
    return AdminPrivacyContext(
        access_tier="operator",
        viewer_person_key="operator",
        allowed_scopes=("public", "operator"),
    )


def _owner() -> AdminPrivacyContext:
    return AdminPrivacyContext(
        access_tier="owner_private",
        viewer_person_key="owner",
        allowed_scopes=("public", "operator", "owner_private"),
    )


def _config() -> PlatformIdentityBlocksSurfaceConfig:
    return PlatformIdentityBlocksSurfaceConfig(
        enabled=True,
        title="Identity Blocks",
        subtitle="Runtime suppression and provider execution posture.",
        status="review",
        status_tone="warn",
        tabs=[
            StatusTab("All", "/identity-blocks", 6, active=True),
            StatusTab("Failed", "/identity-blocks?status=failed", 1, tone="bad"),
        ],
        filters=[
            DashboardFilter("Internal blocked", "/identity-blocks?internal=blocked", key="internal", active=True),
            DashboardFilter("Platform pending", "/identity-blocks?platform=pending", key="platform"),
        ],
        metrics=[
            DashboardMetric("Internal blocked", 2, detail="runtime-owned", tone="bad"),
            DashboardMetric("Provider pending", 1, detail="job queued", tone="warn"),
        ],
        rows=[
            PlatformIdentityBlockRow(
                "blocked-pending",
                "Example chat account",
                "example-chat",
                "Example Person",
                "example-person",
                "known",
                "suppressed",
                "blocked",
                "bad",
                "Runtime policy blocks replies.",
                "1m ago",
                "pending",
                "warn",
                "Provider job queued.",
                "2m ago",
                "Example Provider",
                "job-123",
                "2m",
                "Internal suppression is active while the provider job is still pending.",
                actions=[SurfaceAction("Open", "/identity-blocks/blocked-pending")],
            ),
            PlatformIdentityBlockRow(
                "private-failed",
                "raw private platform identity",
                "example-chat",
                "Owner Private",
                "owner",
                "owner",
                "suppressed",
                "blocked",
                "bad",
                "raw private internal block reason",
                "3m ago",
                "failed",
                "bad",
                "raw private provider block failure",
                "3m ago",
                "Example Provider",
                "job-456",
                "3m",
                "raw private platform summary",
                "/identity-blocks/raw-private",
                privacy_scope="owner_private",
                safe_alternate="Owner-private block row summarized for operators.",
                safe_label="Owner-private identity",
            ),
            PlatformIdentityBlockRow("cancelled", "Cancelled provider job", "example-chat", platform_block_status="cancelled"),
            PlatformIdentityBlockRow("not-requested", "Not requested identity", "example-chat", platform_block_status="not_requested"),
            PlatformIdentityBlockRow("not-applicable", "Not applicable identity", "email", platform_block_status="not_applicable"),
        ],
        sort_key="platform_block_status",
        sort_direction="desc",
        sort_label="Platform block status",
        live_refresh=LiveRefreshConfig(enabled=True, key="identity-blocks", url="/fragments/identity-blocks", target_id="identity-blocks"),
        actions=[SurfaceAction("Refresh posture", "/identity-blocks/refresh", "info", method="post")],
    )


def test_platform_identity_blocks_render_dual_block_states_filters_and_sorting():
    html = render_platform_identity_blocks_surface(
        _config(),
        privacy_policy=_policy(),
        privacy_context=_operator(),
    )

    assert "pc-platform-block-surface" in html
    assert "Identity Blocks" in html
    assert "Internal blocked" in html
    assert "Platform pending" in html
    assert "Sorted by Platform block status" in html
    assert "data-pc-live-controls" in html
    assert "Example chat account" in html
    assert "Internal" in html
    assert "Runtime policy blocks replies." in html
    assert "Platform" in html
    assert "Provider job queued." in html
    assert "Pending" in html
    assert "Failed" in html
    assert "Cancelled" in html
    assert "Not Requested" in html
    assert "Not Applicable" in html
    assert "Refresh posture" in html


def test_platform_identity_blocks_redacts_owner_private_values_for_operator():
    html = render_platform_identity_blocks_surface(
        _config(),
        privacy_policy=_policy(),
        privacy_context=_operator(),
    )

    assert "Owner-private identity" in html
    assert "Owner-private block row summarized for operators." in html
    assert "raw private" not in html
    assert "/identity-blocks/raw-private" not in html


def test_platform_identity_blocks_owner_can_view_private_values_and_href():
    html = render_platform_identity_blocks_surface(
        _config(),
        privacy_policy=_policy(),
        privacy_context=_owner(),
    )

    assert "raw private platform identity" in html
    assert "raw private internal block reason" in html
    assert "raw private provider block failure" in html
    assert "raw private platform summary" in html
    assert "/identity-blocks/raw-private" in html


def test_platform_identity_blocks_feature_gate_and_empty_state():
    config = PlatformIdentityBlocksSurfaceConfig(enabled=True)

    assert platform_identity_blocks_feature_enabled(config, {PLATFORM_IDENTITY_BLOCKS_FEATURE: True}) is True
    assert platform_identity_blocks_feature_enabled(config, {PLATFORM_IDENTITY_BLOCKS_FEATURE: False}) is False
    assert render_platform_identity_blocks_surface(config, features={PLATFORM_IDENTITY_BLOCKS_FEATURE: False}) == ""

    html = render_platform_identity_blocks_surface(config)

    assert "No platform identity block rows configured." in html
