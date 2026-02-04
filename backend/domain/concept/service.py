from datetime import datetime
from uuid import uuid4

from .models import Concept, ConceptVersion
from .rules import can_transition


class ConceptService:

    def create_concept(self, data: dict, created_by: str) -> tuple[Concept, ConceptVersion]:
        concept_id = str(uuid4())
        now = datetime.utcnow()

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

        return concept, version
