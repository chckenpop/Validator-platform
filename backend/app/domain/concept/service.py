from datetime import datetime
from uuid import uuid4
from .models import Concept, ConceptVersion
from .rules import can_transition
from app.domain.common.result import DomainResult
from app.validation.concept_validation import validate_concept_version

class ConceptService:
    """
    Domain service responsible for concept creation,
    versioning, and lifecycle transitions.
    """

    def __init__(self, repository):
        self.repository = repository


    def create_concept(
    self,
    data: dict,
    created_by: str
) -> DomainResult[tuple[Concept, ConceptVersion]]:
        now = datetime.utcnow()
        concept_id = str(uuid4())

        version = ConceptVersion(
            id=str(uuid4()),
            concept_id=concept_id,
            version_number=1,
            name=data["name"],
            core_definition=data["core_definition"],
            expanded_explanation=data["expanded_explanation"],
            learning_objective=data["learning_objective"],
            examples=data.get("examples", []),
            misconceptions=data.get("misconceptions", []),
            scope_boundaries=data.get("scope_boundaries"),
            prerequisites=data.get("prerequisites", []),
            created_by=created_by,
            created_at=now,
            change_note="Initial version"
        )

        concept = Concept(
            id=concept_id,
            current_version=1,
            status="DRAFT",
            created_at=now,
            updated_at=now
        )

        warnings = validate_concept_version(version)

        return DomainResult(
            value=(concept, version),
            warnings=warnings
        )

    def update_concept(
    self,
    concept: Concept,
    latest_version: ConceptVersion,
    data: dict,
    created_by: str,
    change_note: str
) -> DomainResult[tuple[Concept, ConceptVersion]]:
        now = datetime.utcnow()
        next_version_number = latest_version.version_number + 1

        new_version = ConceptVersion(
            id=str(uuid4()),
            concept_id=concept.id,
            version_number=next_version_number,
            name=data.get("name", latest_version.name),
            core_definition=data.get("core_definition", latest_version.core_definition),
            expanded_explanation=data.get(
                "expanded_explanation",
                latest_version.expanded_explanation
            ),
            learning_objective=data.get(
                "learning_objective",
                latest_version.learning_objective
            ),
            examples=data.get("examples", latest_version.examples),
            misconceptions=data.get("misconceptions", latest_version.misconceptions),
            scope_boundaries=data.get(
                "scope_boundaries",
                latest_version.scope_boundaries
            ),
            prerequisites=data.get("prerequisites", latest_version.prerequisites),
            created_by=created_by,
            created_at=now,
            change_note=change_note
        )

        updated_concept = Concept(
            id=concept.id,
            current_version=next_version_number,
            status=concept.status,
            created_at=concept.created_at,
            updated_at=now
        )

        warnings = validate_concept_version(new_version)

        return DomainResult(
            value=(updated_concept, new_version),
            warnings=warnings
        )

    def change_status(
    self,
    concept: Concept,
    new_status: str
) -> DomainResult[Concept]:
        if not can_transition(concept.status, new_status):
            raise ValueError(
                f"Invalid status transition: {concept.status} → {new_status}"
            )

        updated_concept = Concept(
            id=concept.id,
            current_version=concept.current_version,
            status=new_status,
            created_at=concept.created_at,
            updated_at=datetime.utcnow()
        )

        return DomainResult(    
            value=updated_concept,
            warnings=[]
        )
