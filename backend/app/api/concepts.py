from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.application.concept_app_service import ConceptApplicationService
from app.container import get_concept_app_service


router = APIRouter(
    prefix="/concepts",
    tags=["concepts"],
)

# -----------------------------
# Request / Response Schemas
# -----------------------------

class CreateConceptRequest(BaseModel):
    name: str
    core_definition: str
    expanded_explanation: str
    learning_objective: str

    examples: List[str] = []
    misconceptions: List[str] = []
    prerequisites: List[str] = []
    scope_boundaries: Optional[str] = None


class UpdateConceptRequest(BaseModel):
    name: Optional[str] = None
    core_definition: Optional[str] = None
    expanded_explanation: Optional[str] = None
    learning_objective: Optional[str] = None

    examples: Optional[List[str]] = None
    misconceptions: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    scope_boundaries: Optional[str] = None

    change_note: str


class ChangeStatusRequest(BaseModel):
    new_status: str


# -----------------------------
# Routes
# -----------------------------

@router.post("/")
def create_concept(
    payload: CreateConceptRequest,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    Create a new concept (version 1).
    """
    try:
        result = app_service.create_concept(
            data=payload.dict(),
            created_by="system",  # later: auth user
        )

        concept, version = result.value

        return {
            "concept": concept,
            "version": version,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{concept_id}")
def get_concept(
    concept_id: str,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    Get concept + latest version.
    """
    try:
        result = app_service.get_concept(concept_id)
        concept, version = result.value

        return {
            "concept": concept,
            "version": version,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{concept_id}")
def update_concept(
    concept_id: str,
    payload: UpdateConceptRequest,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    Update concept content (creates a new version).
    """
    try:
        data = payload.dict(exclude={"change_note"}, exclude_none=True)

        result = app_service.update_concept(
            concept_id=concept_id,
            data=data,
            created_by="system",
            change_note=payload.change_note,
        )

        concept, version = result.value

        return {
            "concept": concept,
            "version": version,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{concept_id}/status")
def change_status(
    concept_id: str,
    payload: ChangeStatusRequest,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    Change concept lifecycle status.
    """
    try:
        result = app_service.change_status(
            concept_id=concept_id,
            new_status=payload.new_status,
        )

        return {
            "concept": result.value,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{concept_id}/versions")
def list_versions(
    concept_id: str,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    List all versions for a concept.
    """
    try:
        result = app_service.list_versions(concept_id)

        return {
            "versions": result.value,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{concept_id}/versions/{version_number}")
def get_version(
    concept_id: str,
    version_number: int,
    app_service: ConceptApplicationService = Depends(get_concept_app_service),
):
    """
    Get a specific concept version.
    """
    try:
        result = app_service.get_version(concept_id, version_number)

        return {
            "version": result.value,
            "warnings": result.warnings,
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
