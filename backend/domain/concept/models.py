from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class ConceptVersion:
    id: str
    concept_id: str
    version_number: int

    name: str
    core_definition: str
    expanded_explanation: str
    learning_objective: str

    examples: List[str]
    misconceptions: List[str]
    scope_boundaries: Optional[str]
    prerequisites: List[str]

    created_by: str
    created_at: datetime
    change_note: Optional[str]


@dataclass
class Concept:
    id: str
    current_version: int
    status: str  # DRAFT | REVIEW | APPROVED | PUBLISHED
    created_at: datetime
    updated_at: datetime
