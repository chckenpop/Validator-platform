from app.domain.concept.service import ConceptService
from app.application.concept_app_service import ConceptApplicationService

from app.persistence.repositories.sqlite.sqlite_concept_repository import (
    SQLiteConceptRepository,
)
# For dev/testing you can swap this:
# from app.persistence.repositories.in_memory.in_memory_concept_repository import InMemoryConceptRepository


def get_concept_app_service() -> ConceptApplicationService:
    """
    Builds and returns a fully wired ConceptApplicationService.

    This is the single source of truth for backend wiring.
    """

    # Persistence
    repo = SQLiteConceptRepository(db_path="data/app.db")
    # repo = InMemoryConceptRepository()

    # Domain (stateless)
    domain = ConceptService()

    # Application
    return ConceptApplicationService(domain, repo)
