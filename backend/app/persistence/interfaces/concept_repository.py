from typing import Protocol, Optional, List
from app.domain.concept.models import Concept, ConceptVersion


class ConceptRepository(Protocol):
    """
    Repository interface for storing and retrieving Concepts
    and ConceptVersions.

    Implementations MUST respect immutability of ConceptVersion.
    """

    def save_concept(self, concept: Concept) -> None:
        ...

    def save_version(self, version: ConceptVersion) -> None:
        ...

    def get_concept(self, concept_id: str) -> Optional[Concept]:
        ...

    def get_latest_version(self, concept_id: str) -> Optional[ConceptVersion]:
        ...

    def get_version(
        self,
        concept_id: str,
        version_number: int
    ) -> Optional[ConceptVersion]:
        ...

    def list_versions(self, concept_id: str) -> List[ConceptVersion]:
        ...
