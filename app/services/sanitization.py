import bleach

def sanitize_input(text: str) -> str:
    """Sanitize input to prevent XSS."""
    return bleach.clean(text, strip=True)
