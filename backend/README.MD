# Backend — Validator Platform

## Overview
This backend implements the core server-side components for the Validator Platform. It is a small, modular Python service organized around a domain-driven design with a clear separation between API, application logic, domain models/rules, persistence, and validation.

## High-level architecture
- app: application entry and wiring
	- `app/main.py` — application entry (startup)
	- `app/container.py` — dependency wiring / container
- api: HTTP API layer (request/response translation)
	- `app/api/concepts.py` — concept-related HTTP handlers
- application: application services (use-cases)
	- `app/application/concept_app_service.py` — orchestrates domain operations for concepts
- domain: domain model, business rules and domain services
	- `app/domain/concept/models.py` — domain model(s) for the concept entity
	- `app/domain/concept/rules.py` — domain validation rules and business constraints
	- `app/domain/concept/service.py` — domain-level services that implement business logic
	- `app/domain/common/result.py` — result wrapper for success/failure flows
- validation: input and cross-boundary validation
	- `app/validation/concept_validation.py` — validation logic applied to API / application inputs
- persistence: persistence, repository interfaces, and an in-memory implementation
	- `app/persistence/db.py` — DB helper (lightweight abstraction)
	- `app/persistence/interfaces/concept_repository.py` — repository interface for concepts
	- `app/persistence/repositories/in_memory/in_memory_concept_repository.py` — in-memory repo used for tests and as a simple adapter
- core: configuration and shared infra
	- `app/core/config.py` — configuration settings
- migrations: DB schema artifacts
	- `migrations/001_init.sql`
- tests: automated tests for domain/application
	- `tests/domain/test_concept_service.py` — unit tests for concept service

There are also repo-level documents: `API_CONTRACT.md`, `HANDOFFREADME.md`, `TEAMREADME.md` that describe contract and team handoff context.

## Current state of the code (summary)
- The code is small and focused; primary domain is "concepts" with a layered implementation.
- Domain objects and rules are implemented in `app/domain/concept` and wrapped by application services in `app/application`.
- Input validation lives in `app/validation/concept_validation.py` and is designed to be invoked by the API/application layers.
- Persistence currently uses an in-memory repository implementation (`in_memory_concept_repository.py`) which is useful for tests and local runs. There is an abstraction layer (`interfaces/concept_repository.py`) that allows swapping in a real DB-backed repo in the future.
- There's a simple wiring container (`app/container.py`) and `app/main.py` for bootstrapping the app.
- The repository includes a focused unit test `tests/domain/test_concept_service.py` that validates core domain/application behavior.

## How to run and test locally
Prereqs: Python 3.8+ (see `requirements.txt`)

Install dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

Run tests (recommended):

```powershell
cd backend
pytest -q
```

Run the smoke test (quick check):

```powershell
python backend/smoke_test.py
```

Notes:
- The codebase is currently structured for easy unit testing (in-memory persistence), so running tests should not require a DB.
- If you wire a real DB implementation, implement `app/persistence/repositories/<your_adapter>` and update the container wiring in `app/container.py`.

## Design decisions & rationale
- Layered Structure: separates API, application, domain, persistence, and validation for clarity and testability.
- Repository Interface: allows swapping persistence implementations without changing domain logic.
- In-memory repo: speeds local dev and CI, reduces environment setup.
- `Result` wrapper: domain operations use a `Result` pattern (see `app/domain/common/result.py`) to represent success/failure without exceptions for normal control flow.

## Known limitations and TODOs
- Persistence: only an in-memory repo exists. Add a DB-backed repository for production readiness.
- API surface: `app/api/concepts.py` provides handlers but there may be missing HTTP server wiring depending on chosen server framework (e.g., FastAPI, Flask). Confirm framework and add startup integration.
- Configuration: `app/core/config.py` currently holds basic settings; extend with environment-specific configs and secrets handling.
- More tests: expand integration tests and edge-case coverage for validation rules.

## Recommended next steps
- Add a production-ready persistence adapter (Postgres/SQLite) implementing `interfaces/concept_repository.py`.
- Add integration tests that exercise the real DB adapter and API endpoints.
- Add Dockerfile / compose for local environment parity.
- Confirm HTTP framework and add server run instructions (if missing).

## Where to look in the code
- Boot & wiring: [app/main.py](app/main.py), [app/container.py](app/container.py)
- API: [app/api/concepts.py](app/api/concepts.py)
- Application service: [app/application/concept_app_service.py](app/application/concept_app_service.py)
- Domain: [app/domain/concept/models.py](app/domain/concept/models.py), [app/domain/concept/rules.py](app/domain/concept/rules.py), [app/domain/concept/service.py](app/domain/concept/service.py)
- Validation: [app/validation/concept_validation.py](app/validation/concept_validation.py)
- Persistence & repo: [app/persistence/interfaces/concept_repository.py](app/persistence/interfaces/concept_repository.py), [app/persistence/repositories/in_memory/in_memory_concept_repository.py](app/persistence/repositories/in_memory/in_memory_concept_repository.py)
- Tests: [tests/domain/test_concept_service.py](tests/domain/test_concept_service.py)

---
If you'd like, I can:
- Update the existing `backend/README.MD` with this content (replace) instead of creating `backend/README.md`.
- Add a short architecture diagram (text or PlantUML).
- Implement a simple SQLite repository and wiring for quick integration.

Which of these should I do next?
