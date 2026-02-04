## POST /concepts

Creates a new concept in DRAFT state.

### Request body
- name: string (required)
- core_definition: string (required)
- expanded_explanation: string (required)
- learning_objective: string (required)
- examples: list[string] (optional)
- misconceptions: list[string] (optional)
- prerequisites: list[string] (optional)
- scope_boundaries: string (optional)

### Behavior
- Creates Concept (status=DRAFT)
- Creates ConceptVersion (version_number=1)
- No existing data is modified
- Operation is atomic

### Response
- concept
- version
- validation_warnings (list[string])

### Errors
- 400 if required fields missing
- 500 if persistence fails
