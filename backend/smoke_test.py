from app.container import concept_app_service


def main():

    print("\n--- SYSTEM SMOKE TEST ---\n")

    data = {
        "name": "Gravity",
        "core_definition": "Force attracting mass.",
        "expanded_explanation": "Keeps planets in orbit.",
        "learning_objective": "Explain gravity.",
        "examples": ["Apple falling"],
        "misconceptions": ["Only exists on Earth"],
        "prerequisites": ["Basic physics"],
        "scope_boundaries": None,
    }

    # ✅ CREATE
    result = concept_app_service.create_concept(
        data=data,
        created_by="system"
    )

    concept, version = result.value
    warnings = result.warnings

    concept_id = concept.id

    print("✅ Concept created:", concept_id)
    print("Warnings:", warnings)

    # ✅ UPDATE (creates version 2)
    updated_data = {
        "expanded_explanation": "Explains why objects fall and planets orbit."
    }

    result = concept_app_service.update_concept(
        concept_id=concept_id,
        data=updated_data,
        created_by="system",
        change_note="Improved explanation",
    )

    concept, version = result.value
    warnings = result.warnings

    print("✅ Concept updated to version:", version.version_number)

    # ✅ FETCH LATEST
    result = concept_app_service.get_concept(concept_id)

    concept, latest = result.value

    print("✅ Latest version:", latest.version_number)

    # ✅ CHANGE STATUS
    result = concept_app_service.change_status(
        concept_id=concept_id,
        new_status="REVIEW",
    )

    concept = result.value

    print("✅ Status changed to:", concept.status)

    # ✅ LIST VERSIONS
    result = concept_app_service.list_versions(concept_id)

    versions = result.value

    print("✅ Version count:", len(versions))

    print("\n--- SYSTEM BOOT SUCCESSFUL ---\n")


if __name__ == "__main__":
    main()
