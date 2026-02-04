# Validator / Concept Segmentation Platform – Frontend README

## 1. Purpose of this application

This frontend is an **internal tool** used by **concept segmenters and validators** to:

- Read extracted source text
- Create and edit atomic learning concepts
- Review and validate concepts
- Safely approve and publish concepts

⚠️ This is **NOT** a learner-facing application.

---

## 2. Design philosophy (non-negotiable)

- **Reliability > Speed > Visual polish**
- Text-first, dense, IDE-like UI
- Explicit actions over implicit automation
- Prevent accidental destructive actions

Mental reference:  
> GitHub PR review / admin dashboard, not a consumer app.

---

## 3. Users & roles (frontend-relevant)

Frontend should assume the backend provides the role.

**Roles:**
- Viewer (read-only)
- Editor (can edit drafts)
- Validator (can approve/reject)
- Publisher (can publish approved concepts)

UI must **disable or hide actions** the role is not allowed to perform.

---

## 4. Core layout (canonical)

This layout is fixed across the app.

┌──────────────────────────────────────────────┐
│ Top Bar: Project | Status | Save | Publish │
├───────────────┬───────────────┬─────────────┤
│ Left Panel │ Center Panel │ Right Panel │
│ Source Text │ Concept Editor│ Meta/Safety │
├───────────────┴───────────────┴─────────────┤
│ Bottom Panel (collapsible): │
│ Warnings | Comments | Diff | History │
└──────────────────────────────────────────────┘


**Rules:**
- Panels are resizable
- Top bar is always visible
- Center panel is primary focus
- No major layout changes between screens

---

## 5. Main UI sections

### 5.1 Top Bar

Always visible.

**Contains:**
- Current concept set / chapter name
- Concept status: Draft / Review / Approved / Published
- Autosave indicator
- **Save** (manual)
- **Send to Review**
- **Publish** (guarded with confirmation)

**Publish button rules:**
- Disabled unless state = Approved
- Must show confirmation modal

---

### 5.2 Left Panel – Source Text (Read-only)

**Purpose:** context only.

**Features:**
- Extracted plain text
- Paragraph IDs
- Text selection
- “Create concept from selection” action

**Restrictions:**
- ❌ No editing
- ❌ No formatting changes

---

### 5.3 Center Panel – Concept Editor (Primary)

Structured editor (**NOT** a single freeform text area).

#### Required fields
- Concept Name (text)
- Core Definition (textarea, character-limited)
- Expanded Explanation (textarea)
- Learning Objective (textarea, verb-based hint)

#### Optional fields
- Examples (repeatable block)
- Common Misconceptions (repeatable block)
- Scope Boundaries (“This concept does NOT include…”)

Each field must support:
- Label + helper text
- Validation error state
- Read-only mode when concept is Published

Notes:
- Markdown / LaTeX allowed
- No WYSIWYG editors

---

### 5.4 Right Panel – Meta & Safety

Always visible.

**Shows:**
- Prerequisites (list, editable)
- Downstream dependencies (read-only)
- Concept size indicator (small / ok / large)
- Overlap warnings
- Role-based permissions
- Status history

Warnings should be visible and noticeable, but not modal by default.

---

### 5.5 Bottom Panel (Collapsible)

**Tabs:**
- Validation Warnings
- Review Comments
- Version Diff (side-by-side)
- Change History

**Diff view:**
- Old vs new version
- Highlight text changes

---

## 6. Concept lifecycle & UI states

**Concept states:**
1. Draft
2. In Review
3. Approved
4. Published

### Button availability

| State      | Editable | Actions                                  |
|------------|----------|-------------------------------------------|
| Draft      | Yes      | Save, Send to Review                      |
| Review     | No       | Comment, Approve, Request Changes         |
| Approved   | No       | Publish                                  |
| Published  | No       | View only                                |

No other transitions are allowed in UI.

---

## 7. Sample data (frontend can hardcode initially)

Frontend should work with mocked data.

```json
{
  "id": "concept_001",
  "name": "Numerator",
  "definition": "The top number in a fraction...",
  "explanation": "In 3/4, the numerator is 3...",
  "learningObjective": "Identify the numerator in a fraction",
  "prerequisites": ["Fraction - Basic Definition"],
  "status": "Draft",
  "warnings": [
    "Uses example shared with another concept"
  ],
  "version": 2
}

8. UX constraints (important)

No hidden destructive actions

Autosave + manual save must both exist

Publishing requires explicit confirmation

Read-only state must be visually obvious

Keyboard navigation encouraged (tab order matters)

9. Explicit non-goals (do not implement)

Learner previews

Animations

Gamification

Visual content editing

Auto-publish flows

