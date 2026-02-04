ALLOWED_STATUS_TRANSITIONS = {
    "DRAFT": {"REVIEW"},
    "REVIEW": {"APPROVED"},
    "APPROVED": {"PUBLISHED"},
    "PUBLISHED": set()
}


def can_transition(current_status: str, next_status: str) -> bool:
    return next_status in ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
