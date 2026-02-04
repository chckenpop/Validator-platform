# Infrastructure Handoff – Validator Platform Backend

## Audience

This document is for:
- Infrastructure / backend engineers
- AI tools generating infrastructure code

It defines **non-negotiable domain invariants** that infrastructure code MUST respect.

If infrastructure behavior conflicts with this document, **the infrastructure is wrong**.

---

## System Overview (Context)

This backend stores and manages **validated learning concepts**.

Key characteristics:
- Concepts are versioned
- Content is immutable
- Humans are in the loop
- Correctness and auditability are higher priority than speed or convenience

---

## Core Domain Objects (Read-Only Knowledge)

### Concept
- Represents identity + lifecycle
- Fields:
  - `id`
  - `current_version`
  - `status` (DRAFT | REVIEW | APPROVED | PUBLISHED)
  - timestamps
- **Does NOT store content**

### ConceptVersion
- Represents immutable content snapshot
- Fields include:
  - definition, explanation, examples, prerequisites, etc.
- **MUST NEVER be updated after creation**

---

## Absolute Rules (NON-NEGOTIABLE)

### 1️⃣ Immutability
- There must be **NO UPDATE statements** on `ConceptVersion`
- Content edits ALWAYS create a new version row
- Old versions must remain untouched forever

### 2️⃣ Versioning Semantics
- Creating a concept → version_number = 1
- Editing content → version_number increments by 1
- Changing status → does NOT create a new content version

### 3️⃣ Lifecycle Enforcement
Allowed transitions only:

# Infrastructure Handoff – Validator Platform Backend

## Audience

This document is for:
- Infrastructure / backend engineers
- AI tools generating infrastructure code

It defines **non-negotiable domain invariants** that infrastructure code MUST respect.

If infrastructure behavior conflicts with this document, **the infrastructure is wrong**.

---

## System Overview (Context)

This backend stores and manages **validated learning concepts**.

Key characteristics:
- Concepts are versioned
- Content is immutable
- Humans are in the loop
- Correctness and auditability are higher priority than speed or convenience

---

## Core Domain Objects (Read-Only Knowledge)

### Concept
- Represents identity + lifecycle
- Fields:
  - `id`
  - `current_version`
  - `status` (DRAFT | REVIEW | APPROVED | PUBLISHED)
  - timestamps
- **Does NOT store content**

### ConceptVersion
- Represents immutable content snapshot
- Fields include:
  - definition, explanation, examples, prerequisites, etc.
- **MUST NEVER be updated after creation**

---

## Absolute Rules (NON-NEGOTIABLE)

### 1️⃣ Immutability
- There must be **NO UPDATE statements** on `ConceptVersion`
- Content edits ALWAYS create a new version row
- Old versions must remain untouched forever

### 2️⃣ Versioning Semantics
- Creating a concept → version_number = 1
- Editing content → version_number increments by 1
- Changing status → does NOT create a new content version

### 3️⃣ Lifecycle Enforcement
Allowed transitions only:

DRAFT → REVIEW → APPROVED → PUBLISHED


- No skipping states
- No backward transitions
- Backend must enforce this (frontend is not trusted)

---

## Repository Contract (Must Be Implemented As-Is)

Infrastructure must implement the following interface:

```python
class ConceptRepository(Protocol):

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

Do NOT add fields

Do NOT change method semantics

Do NOT collapse Concept and ConceptVersion into one table

Database Guidance (Recommended, Not Mandatory)

SQLite is acceptable and recommended for v1

PostgreSQL-compatible schema preferred for future migration

Use transactions for:

concept creation

version creation

status changes

Validation Integration

Domain validation exists as warnings, not blockers.

Infrastructure may:

Call validation on save

Store warnings

Return warnings to API consumers

Infrastructure must NOT:

Convert warnings into hard errors

Auto-fix content

Humans decide.

What Infrastructure Must NOT Do

❌ Overwrite concept content
❌ Auto-increment versions without domain input
❌ Change status implicitly
❌ Enforce business rules outside the domain layer
❌ Invent new lifecycle states

Failure Modes to Avoid (Important)

Partial writes (concept saved but version not saved)

Silent overwrites

Skipped lifecycle states

Schema changes without domain approval

Definition of Success (v1)

Infrastructure is correct if:

History can be reconstructed

Versions can be diffed

Invalid state transitions are blocked

No content is ever lost

Performance and polish are secondary.

Final Rule

If infrastructure behavior makes the system more convenient but less correct,
do not do it.

Correctness wins.


---

## What to do with this doc (important)

1. Save it as:


backend/INFRA_HANDOFF.md


2. Commit it:
```bash
git add backend/INFRA_HANDOFF.md
git commit -m "docs: add infrastructure handoff and invariants"


Send it to your backend friend and say:

“This defines the rules. Please implement infra to match this.”

Paste it into any AI prompt that generates:

SQL schemas

Repository implementations

FastAPI routes