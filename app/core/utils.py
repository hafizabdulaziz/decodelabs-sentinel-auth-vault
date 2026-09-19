def normalize_email(email: str) -> str:
    """Normalize email: lowercase and strip whitespace."""
    return email.strip().lower()
