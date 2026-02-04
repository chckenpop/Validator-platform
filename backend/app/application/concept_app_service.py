from app.domain.common.result import DomainResult

class ConceptAppService:

    def __init__(self, domain_service, repository):
        self.domain = domain_service
        self.repo = repository


    # -----------------------------
    # CREATE
    # -----------------------------
    def create_concept(self, data: dict, created_by: str):
        result = self.domain.create_concept(
            data=data,
            created_by=created_by
        )

        concept, version = result.value

        self.repo.save_concept(concept)
        self.repo.save_version(version)

        return result

    # -----------------------------
    # GET LATEST
    # -----------------------------

    def get_concept(self, concept_id: str):

        concept = self.repo.get_concept(concept_id)

        if concept is None:
            raise ValueError("Concept not found")

        version = self.repo.get_latest_version(concept_id)

        return DomainResult(
            value = (concept, version),
            warnings = []
        )



    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_concept(
        self,
        concept_id: str,
        data: dict,
        created_by: str,
        change_note: str,
    ):

        if not change_note:
            raise ValueError("change_note is required")

        concept = self.repo.get_concept(concept_id)
        latest = self.repo.get_latest_version(concept_id)

        if concept is None or latest is None:
            raise ValueError("Concept not found")

        result = self.domain.update_concept(
            concept,
            latest,
            data,
            created_by,
            change_note,
        )

        concept, version = result.value

        self.repo.save_concept(concept)
        self.repo.save_version(version)

        return result



    # -----------------------------
    # STATUS
    # -----------------------------
    def change_status(self, concept_id: str, new_status: str):

        concept = self.repo.get_concept(concept_id)

        if concept is None:
            raise ValueError("Concept not found")

        result = self.domain.change_status(concept, new_status)

        updated_concept = result.value

        self.repo.save_concept(updated_concept)

        return result



    # -----------------------------
    # LIST VERSIONS
    # -----------------------------
    def list_versions(self, concept_id: str):

        concept = self.repo.get_concept(concept_id)

        if concept is None:
            raise ValueError("Concept not found")

        versions = self.repo.list_versions(concept_id)

        return DomainResult(
            value = versions,
            warnings = []
        )



    # -----------------------------
    # GET VERSION
    # -----------------------------
    def get_version(self, concept_id: str, version_number: int):

        version = self.repo.get_version(concept_id, version_number)

        if version is None:
            raise ValueError("Version not found")

        return DomainResult(
            value=version,
            warnings=[]
            )

