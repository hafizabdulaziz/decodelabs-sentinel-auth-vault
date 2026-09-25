import re

from fastapi import HTTPException, status


def validate_password_complexity(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def verify_password_strength(password: str):
    if not validate_password_complexity(password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password does not meet complexity requirements (min 8 chars, 1 uppercase, 1 special char, 1 number)",
        )
