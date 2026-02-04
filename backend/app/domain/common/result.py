from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class DomainResult(Generic[T]):
    """
    Standard wrapper for domain operations.

    - value: the primary domain result
    - warnings: non-blocking validation warnings
    """
    value: T
    warnings: List[str]
