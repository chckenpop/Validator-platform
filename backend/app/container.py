from app.persistence.interfaces.concept_repository import ConceptRepository
from app.persistence.repositories.in_memory.in_memory_concept_repository import (
    InMemoryConceptRepository,
)

from app.domain.concept.service import ConceptService
from app.application.concept_app_service import ConceptAppService

from app.persistence.repositories.sqlite.sqlite_concept_repository import (
    SQLiteConceptRepository
)
from app.application.concept_app_service import ConceptApplicationService

def build_concept_app_service():
    repo = SQLiteConceptRepository(db_path="data/app.db")
    return ConceptApplicationService(repo)

# Repository
concept_repository: ConceptRepository = InMemoryConceptRepository()

# Domain Service
concept_domain_service = ConceptService(concept_repository)

# Application Service
concept_app_service = ConceptAppService(concept_domain_service,concept_repository)