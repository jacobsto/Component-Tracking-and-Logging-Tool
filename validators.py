# Validation helpers to keep UI and services clean.

from errors import ValidationError # imports from error.py
from models import ALLOWED_STATUSES # imports from models.py

# Ensure text is non-empty after trimming.
def require_non_empty(text: str, field_name: str) -> str:
    if text is None or str(text).strip() == "":
        raise ValidationError(f"{field_name} cannot be empty.")
    return str(text).strip()

# Convert text to integer, raising error if invalid.
def to_int(text: str, field_name: str) -> int:
    try:
        return int(str(text).strip())
    except ValueError as ex:
        raise ValidationError(f"{field_name} must be an integer.") from ex

# Ensure integer meets minimum value.    
def require_min(value: int, minimum: int, field_name: str) -> int:
    if value < minimum:
        raise ValidationError(f"{field_name} must be at least >= {minimum}.")
    return value

# Parse comma-separated tags into a list.
def parse_tags(text: str) -> list:
    if text is None or text.strip() == "":
        return []
    parts = text.split(",")
    return [p.strip() for p in parts if p.strip()]