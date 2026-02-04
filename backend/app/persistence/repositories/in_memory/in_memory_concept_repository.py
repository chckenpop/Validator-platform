from typing import Dict, Optional, List
from copy import deepcopy

from app.domain.concept.models import Concept, ConceptVersion
from app.persistence.interfaces.concept_repository import ConceptRepository


class InMemoryConceptRepository(ConceptRepository):
    """
    In-memory aggregate repository.

    Guarantees:
    - No silent overwrites
    - Immutable version storage
    - Deterministic retrieval
    - Versions cannot exist without a Concept
    """

    def __init__(self) -> None:
        self._concepts: Dict[str, Concept] = {}
        self._versions: Dict[str, Dict[int, ConceptVersion]] = {}

    # -------------------------
    # Concept Methods
    # -------------------------

    def save_concept(self, concept: Concept) -> None:
        self._concepts[concept.id] = deepcopy(concept)

        if concept.id not in self._versions:
            self._versions[concept.id] = {}

    def get_concept(self, concept_id: str) -> Optional[Concept]:
        concept = self._concepts.get(concept_id)

        if concept is None:
            return None

        return deepcopy(concept)

    # -------------------------
    # Version Methods
    # -------------------------

    def save_version(self, version: ConceptVersion) -> None:
        concept_id = version.concept_id

        if concept_id not in self._versions:
            raise ValueError("Concept does not exist")

        versions = self._versions[concept_id]

        if version.version_number in versions:
            raise ValueError("Version already exists")

        versions[version.version_number] = deepcopy(version)

    def get_latest_version(self, concept_id: str) -> Optional[ConceptVersion]:
        versions = self._versions.get(concept_id)

        if versions is None:
            return None

        if len(versions) == 0:
            return None

        latest_number = max(versions.keys())
        return deepcopy(versions[latest_number])

    def get_version(self, concept_id: str, version_number: int) -> Optional[ConceptVersion]:
        versions = self._versions.get(concept_id)

        if versions is None:
            return None

        version = versions.get(version_number)
        if version is None:
            return None

        return deepcopy(version)


    def list_versions(self, concept_id: str) -> List[ConceptVersion]:
        versions = self._versions.get(concept_id)

        if not versions:
            return []

        return [deepcopy(v) for v in versions.values()]
