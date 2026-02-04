# Team README – Validator Platform Backend

## Purpose of this document

This README defines **how we build**, **who owns what**, and **what rules cannot be broken** while developing the backend for the Validator / Concept Segmentation Platform.

This document is authoritative for:
- Human collaborators
- AI-assisted code generation

If something conflicts with this README, **this README wins**.

---

## What we are building (context)

We are building a **knowledge validation backend**, not a CRUD app.

Core ideas:
- Knowledge is represented as **atomic concepts**
- Concept content is **immutable via versioning**
- Humans define meaning
- The backend enforces correctness and history
- The frontend is a client, not an authority

---

## Core architectural principles (NON-NEGOTIABLE)

1. **Concepts are versioned**
   - Content is never overwritten
   - Edits create new versions
   - Old versions are immutable

2. **Concept identity is separate from content**
   - `Concept` = identity + lifecycle
   - `ConceptVersion` = content snapshot

3. **Domain logic is framework-agnostic**
   - No HTTP logic in domain
   - No database logic in domain

4. **Backend enforces rules**
   - Frontend only reflects state
   - Backend decides what is allowed

5. **Correctness > speed > convenience**

---

## Repository structure (must be respected)


---

## Ownership & responsibilities

### Domain owner (Concepts, versions, rules)
Responsible for:
- Data models
- Versioning semantics
- State transitions
- Business rules
- Validation meaning

Works mainly in:

app/domain/
app/validation/ 


**Any change that affects meaning must be reviewed by the domain owner.**

---

### Infrastructure / API owner
Responsible for:
- Database integration
- Repositories
- FastAPI routes
- Dependency injection
- Error handling

Works mainly in:

app/persistence/
app/api/
app/main.py


**Infrastructure must not invent business rules.**

---

## Data model rules (CRITICAL)

### Concept
- Represents identity and lifecycle
- Does NOT store content

### ConceptVersion
- Represents immutable content
- One version = one snapshot
- NEVER updated after creation

### Absolute rule
> **There must be no UPDATE statements on ConceptVersion records. Ever.**

If content changes, create a new version.

---

## State machine (must not be bypassed)

Allowed transitions only:

DRAFT → REVIEW → APPROVED → PUBLISHED


- No skipping states
- No backward transitions
- Backend enforces this

---

## Development order (do not deviate)

1. Domain models (`domain/concept/models.py`)
2. State rules (`domain/concept/rules.py`)
3. Domain services (`domain/concept/service.py`)
4. Persistence repositories
5. API routes
6. Validation intelligence
7. Everything else

If step 1–3 are not solid, **do not proceed**.

---

## Coding rules (important)

### Domain layer
- No FastAPI imports
- No SQL / ORM imports
- No side effects
- Pure logic only

### API layer
- Thin controllers
- No business logic
- Translate HTTP → domain calls

### Persistence layer
- No business rules
- No state transitions
- Store exactly what domain gives

---

## Versioning semantics (lock this in)

- Creating a concept → version 1
- Editing content → new version (N+1)
- Changing status → does NOT create a new content version
- Published concepts are read-only

---

## What we deliberately do NOT build early

- Auth & permissions (can be mocked)
- AI integration
- Graph visualizations
- Performance optimizations
- Advanced diff UI

These are **future concerns**, not v1 requirements.

---

## Git & collaboration rules

- Small PRs only
- No direct commits to `main`
- Domain owner reviews domain changes
- Infra owner reviews API/persistence changes
- Do not edit the same file in parallel

---

## How to use AI safely on this project

When asking AI to generate code:
- Provide this README
- Specify the exact file to modify
- Specify the layer (domain / api / persistence)
- Do NOT ask AI to invent rules or schemas

AI is allowed to:
- Write boilerplate
- Implement agreed interfaces
- Fill in repetitive code

AI is NOT allowed to:
- Change data model meaning
- Modify versioning rules
- Invent state transitions

---

## Definition of “done” for v1

V1 is successful if:
- Concepts can be created as drafts
- Content edits create new versions
- Status transitions are enforced
- History is preserved
- The system can explain its own rules

Polish is optional. Correctness is not.

---

## Final rule (read this last)

> If something feels convenient but weakens correctness, **do not do it**.

This backend is the source of truth.
