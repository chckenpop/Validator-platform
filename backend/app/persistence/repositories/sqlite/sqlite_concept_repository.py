from datetime import datetime
import json
from typing import Optional
from app.domain.concept.models import Concept, ConceptVersion
from app.persistence.interfaces.concept_repository import ConceptRepository
from app.persistence.db import get_connection
import os

class SQLiteConceptRepository(ConceptRepository):
    def __init__(self, db_path: str):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path


    def save_concept(self, concept: Concept) -> None:
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO concepts (id, current_version, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    current_version = excluded.current_version,
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    concept.id,
                    concept.current_version,
                    concept.status,
                    concept.created_at.isoformat(),
                    concept.updated_at.isoformat(),
                ),
            )

    def save_version(self, version: ConceptVersion) -> None:
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO concept_versions (
                    id, concept_id, version_number,
                    name, core_definition, expanded_explanation,
                    learning_objective, examples, misconceptions,
                    prerequisites, scope_boundaries,
                    created_by, created_at, change_note
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version.id,
                    version.concept_id,
                    version.version_number,
                    version.name,
                    version.core_definition,
                    version.expanded_explanation,
                    version.learning_objective,
                    json.dumps(version.examples),
                    json.dumps(version.misconceptions),
                    json.dumps(version.prerequisites),
                    version.scope_boundaries,
                    version.created_by,
                    version.created_at.isoformat(),
                    version.change_note,
                ),
            )

    def get_concept(self, concept_id: str) -> Optional[Concept]:
        with get_connection(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM concepts WHERE id = ?",
                (concept_id,),
            ).fetchone()

        if not row:
            return None

        return Concept(
            id=row["id"],
            current_version=row["current_version"],
            status=row["status"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def get_latest_version(self, concept_id: str) -> Optional[ConceptVersion]:
        with get_connection(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT *
                FROM concept_versions
                WHERE concept_id = ?
                ORDER BY version_number DESC
                LIMIT 1
                """,
                (concept_id,),
            ).fetchone()

        if not row:
            return None

        return ConceptVersion(
            id=row["id"],
            concept_id=row["concept_id"],
            version_number=row["version_number"],
            name=row["name"],
            core_definition=row["core_definition"],
            expanded_explanation=row["expanded_explanation"],
            learning_objective=row["learning_objective"],
            examples=json.loads(row["examples"]),
            misconceptions=json.loads(row["misconceptions"]),
            prerequisites=json.loads(row["prerequisites"]),
            scope_boundaries=row["scope_boundaries"],
            created_by=row["created_by"],
            created_at=datetime.fromisoformat(row["created_at"]),
            change_note=row["change_note"],
        )
    
    def list_versions(self, concept_id: str):

        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM concept_versions
                WHERE concept_id = ?
                ORDER BY version_number ASC
                """,
                (concept_id,),
            ).fetchall()

        versions = []

        for row in rows:
            versions.append(
                ConceptVersion(
                    id=row["id"],
                    concept_id=row["concept_id"],
                    version_number=row["version_number"],
                    name=row["name"],
                    core_definition=row["core_definition"],
                    expanded_explanation=row["expanded_explanation"],
                    learning_objective=row["learning_objective"],
                    examples=json.loads(row["examples"]),
                    misconceptions=json.loads(row["misconceptions"]),
                    prerequisites=json.loads(row["prerequisites"]),
                    scope_boundaries=row["scope_boundaries"],
                    created_by=row["created_by"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    change_note=row["change_note"],
                )
            )

        return versions

