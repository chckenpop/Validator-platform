import pytest
from app.domain.concept.service import ConceptService
from app.domain.concept.models import ConceptVersion


@pytest.fixture
def service():
    return ConceptService()


@pytest.fixture
def base_data():
    return {
        "name": "Numerator",
        "core_definition": "The top number in a fraction.",
        "expanded_explanation": "It tells how many parts are taken.",
        "learning_objective": "Identify the numerator in a fraction",
        "examples": ["In 3/4, the numerator is 3"],
        "misconceptions": [],
        "prerequisites": ["Fraction"]
    }


def test_create_concept_creates_version_1(service, base_data):
    concept, version = service.create_concept(base_data, created_by="tester")

    assert concept.current_version == 1
    assert concept.status == "DRAFT"

    assert isinstance(version, ConceptVersion)
    assert version.version_number == 1
    assert version.name == "Numerator"


def test_update_concept_creates_new_version(service, base_data):
    concept, v1 = service.create_concept(base_data, created_by="tester")

    updated_data = {
        "core_definition": "The number above the line in a fraction."
    }

    concept, v2 = service.update_concept(
        concept,
        v1,
        updated_data,
        created_by="tester",
        change_note="Clarified definition"
    )

    assert v1.version_number == 1
    assert v2.version_number == 2

    # Old version must remain unchanged
    assert v1.core_definition == "The top number in a fraction."
    assert v2.core_definition == "The number above the line in a fraction."

    # Concept should point to the new version
    assert concept.current_version == 2


def test_update_does_not_change_status(service, base_data):
    concept, v1 = service.create_concept(base_data, created_by="tester")

    concept, v2 = service.update_concept(
        concept,
        v1,
        {},
        created_by="tester",
        change_note="No-op edit"
    )

    assert concept.status == "DRAFT"


def test_valid_status_transition(service, base_data):
    concept, _ = service.create_concept(base_data, created_by="tester")

    concept = service.change_status(concept, "REVIEW")

    assert concept.status == "REVIEW"


def test_invalid_status_transition_raises(service, base_data):
    concept, _ = service.create_concept(base_data, created_by="tester")

    with pytest.raises(ValueError):
        service.change_status(concept, "PUBLISHED")
