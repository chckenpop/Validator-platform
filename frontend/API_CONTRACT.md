Validation Warnings

Always returned as a list of strings

Never block creation or updates

Frontend decides how to display them

Endpoints
POST /concepts

Create a new concept in DRAFT state.

Request Body
{
  "name": "string (required)",
  "core_definition": "string (required)",
  "expanded_explanation": "string (required)",
  "learning_objective": "string (required)",
  "examples": ["string"],
  "misconceptions": ["string"],
  "prerequisites": ["string"],
  "scope_boundaries": "string"
}

Behavior

Creates a new Concept

Sets status = DRAFT

Creates ConceptVersion with version_number = 1

Operation must be atomic

No existing data is modified

Response (201)
{
  "concept": {
    "id": "uuid",
    "current_version": 1,
    "status": "DRAFT",
    "created_at": "iso-timestamp",
    "updated_at": "iso-timestamp"
  },
  "version": {
    "version_number": 1,
    "name": "Numerator",
    "core_definition": "...",
    "expanded_explanation": "...",
    "learning_objective": "...",
    "examples": [],
    "misconceptions": [],
    "prerequisites": [],
    "scope_boundaries": "...",
    "created_at": "iso-timestamp",
    "change_note": "Initial version"
  },
  "validation_warnings": []
}

Errors

400 – Missing required fields

500 – Persistence failure

GET /concepts/{concept_id}

Fetch the latest version of a concept.

Behavior

Returns Concept + latest ConceptVersion

Does not modify state

Response (200)
{
  "concept": { ... },
  "version": { ... }
}

Errors

404 – Concept not found

PUT /concepts/{concept_id}

Update concept content (creates a new version).

Request Body
{
  "name": "string (optional)",
  "core_definition": "string (optional)",
  "expanded_explanation": "string (optional)",
  "learning_objective": "string (optional)",
  "examples": ["string"],
  "misconceptions": ["string"],
  "prerequisites": ["string"],
  "scope_boundaries": "string",
  "change_note": "string (required)"
}

Behavior

Creates a new ConceptVersion

Increments version_number by 1

Does NOT modify old versions

Does NOT change lifecycle status

Operation must be atomic

Response (200)
{
  "concept": { ... },
  "version": { ... },
  "validation_warnings": []
}

Errors

400 – Missing change_note

404 – Concept not found

500 – Persistence failure

POST /concepts/{concept_id}/status

Change the lifecycle status of a concept.

Request Body
{
  "new_status": "REVIEW | APPROVED | PUBLISHED"
}

Behavior

Validates transition using domain rules

Does NOT create a new ConceptVersion

Does NOT modify content

Response (200)
{
  "concept": {
    "id": "uuid",
    "current_version": 3,
    "status": "REVIEW",
    "updated_at": "iso-timestamp"
  }
}

Errors

400 – Invalid transition

404 – Concept not found

GET /concepts/{concept_id}/versions

List all versions of a concept.

Behavior

Returns versions in ascending order

Read-only

Response (200)
{
  "versions": [
    { "version_number": 1, "created_at": "..." },
    { "version_number": 2, "created_at": "..." }
  ]
}

GET /concepts/{concept_id}/versions/{version_number}

Fetch a specific historical version.

Behavior

Read-only

Does not affect lifecycle or current_version

Response (200)
{
  "version": { ... }
}

Errors

404 – Version not found

Non-Goals for v1 (Explicitly Out of Scope)

Authentication / authorization

Role enforcement

Draft locking

Publishing to learners

Soft deletes

Partial updates without versioning

Invariants (Must Hold for All Endpoints)

No content is ever overwritten

Version history is complete

Lifecycle rules are enforced by backend

Validation warnings never block

Transactions are atomic

Final Rule

If an API shortcut makes implementation easier but violates
domain invariants, do not take the shortcut.

Correctness wins.


---

### What to do now (practical)

1. Save this as  


backend/API_CONTRACT.md


2. Commit it  
```bash
git add backend/API_CONTRACT.md
git commit -m "docs: add v1 API contract"