"""Consumer integration doctor re-export for the public PersonaCore import path."""

from persona_console.doctor import (
    ConsumerIntegrationDoctorReport,
    DoctorCheck,
    ModuleSnapshot,
    doctor_report_to_text,
    main,
    run_consumer_integration_doctor,
)

__all__ = [
    "ConsumerIntegrationDoctorReport",
    "DoctorCheck",
    "ModuleSnapshot",
    "doctor_report_to_text",
    "main",
    "run_consumer_integration_doctor",
]
