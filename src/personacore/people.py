"""People surface re-exports for the public PersonaCore import path."""

from persona_console.models import (
    PeopleSurfaceConfig,
    PersonListRow,
    PersonRelationshipSummary,
    PersonTag,
)
from persona_console.people import (
    PEOPLE_FEATURE,
    people_surface_feature_enabled,
    render_people_surface,
)

__all__ = [
    "PEOPLE_FEATURE",
    "PeopleSurfaceConfig",
    "PersonListRow",
    "PersonRelationshipSummary",
    "PersonTag",
    "people_surface_feature_enabled",
    "render_people_surface",
]
