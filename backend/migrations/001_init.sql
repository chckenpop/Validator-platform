CREATE TABLE concepts (
    id TEXT PRIMARY KEY,
    current_version INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE concept_versions (
    id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,

    name TEXT NOT NULL,
    core_definition TEXT NOT NULL,
    expanded_explanation TEXT NOT NULL,
    learning_objective TEXT NOT NULL,
    examples TEXT NOT NULL,
    misconceptions TEXT NOT NULL,
    prerequisites TEXT NOT NULL,
    scope_boundaries TEXT,
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    change_note TEXT,

    FOREIGN KEY (concept_id) REFERENCES concepts(id),
    UNIQUE (concept_id, version_number)
);
