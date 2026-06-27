"""Journal surface re-exports for the public PersonaCore import path."""

from persona_console.journal import (
    JOURNAL_FEATURE,
    JOURNAL_THEME_KEYS,
    build_journal_calendar,
    journal_surface_feature_enabled,
    journal_theme_key,
    journal_theme_options,
    render_journal_surface,
)
from persona_console.models import (
    JournalCalendarDay,
    JournalDetail,
    JournalEntry,
    JournalMarker,
    JournalSurfaceConfig,
    JournalThemeOption,
)

__all__ = [
    "JOURNAL_FEATURE",
    "JOURNAL_THEME_KEYS",
    "JournalCalendarDay",
    "JournalDetail",
    "JournalEntry",
    "JournalMarker",
    "JournalSurfaceConfig",
    "JournalThemeOption",
    "build_journal_calendar",
    "journal_surface_feature_enabled",
    "journal_theme_key",
    "journal_theme_options",
    "render_journal_surface",
]
