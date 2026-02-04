from typing import List
from app.domain.concept.models import ConceptVersion


def validate_concept_version(version: ConceptVersion) -> List[str]:
    """
    Runs domain-level validation checks on a ConceptVersion.

    Returns a list of human-readable warning messages.
    Does NOT raise exceptions.
    """
    warnings: List[str] = []

    # --- Length & structure checks ---

    if len(version.core_definition.strip()) == 0:
        warnings.append("Core definition is empty")

    if len(version.core_definition) > 300:
        warnings.append("Core definition may be too long")

    if len(version.expanded_explanation.strip()) == 0:
        warnings.append("Expanded explanation is empty")

    # --- Learning objective checks ---

    if len(version.learning_objective.strip()) == 0:
        warnings.append("Learning objective is missing")

    if not version.learning_objective.lower().startswith(
        ("identify", "explain", "describe", "calculate", "compare")
    ):
        warnings.append(
            "Learning objective should start with an observable verb "
            "(e.g., identify, explain, calculate)"
        )

    # --- Concept clarity checks ---

    if version.name.lower() in version.core_definition.lower():
        warnings.append(
            "Core definition may be circular (concept name appears in definition)"
        )

    if len(version.examples) == 0:
        warnings.append("No examples provided")

    # --- Dependency checks ---

    if "fraction" in version.core_definition.lower() and not version.prerequisites:
        warnings.append(
            "Concept references other ideas but has no prerequisites listed"
        )

    # --- Scope checks ---

    if version.scope_boundaries is None or len(version.scope_boundaries.strip()) == 0:
        warnings.append("Scope boundaries are not defined")

    return warnings
