"""Dashboard primitive re-exports for the public PersonaCore import path."""

from persona_console.dashboard import (
    render_dashboard_activity,
    render_dashboard_adapter_cards,
    render_dashboard_attention,
    render_dashboard_filters,
    render_dashboard_flow,
    render_dashboard_health_strip,
    render_dashboard_metrics,
    render_dashboard_queue,
    render_dashboard_route_cards,
    render_dashboard_sections,
)

__all__ = [
    "render_dashboard_activity",
    "render_dashboard_adapter_cards",
    "render_dashboard_attention",
    "render_dashboard_filters",
    "render_dashboard_flow",
    "render_dashboard_health_strip",
    "render_dashboard_metrics",
    "render_dashboard_queue",
    "render_dashboard_route_cards",
    "render_dashboard_sections",
]
