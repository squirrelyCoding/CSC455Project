import string
import secrets
from typing import Dict, List


def generate_password(length: int = 16) -> str:
    if length < 12:
        raise ValueError("Your password must be at least 12 characters long.")
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_strong_password(length: int = 16) -> str:
    # Ensure at least one character from each category
    if length < 12:
        raise ValueError("Your password must be at least 12 characters long.")
    categories = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    # Start with one guaranteed char from each category
    pwd_chars = [secrets.choice(cat) for cat in categories]
    remaining = length - len(pwd_chars)
    all_chars = ''.join(categories)
    pwd_chars += [secrets.choice(all_chars) for _ in range(remaining)]
    # Shuffle securely
    secrets.SystemRandom().shuffle(pwd_chars)
    return ''.join(pwd_chars)


def check_strength(password: str) -> Dict[str, object]:
    suggestions: List[str] = []
    length = len(password)
    score = 0

    # Length scoring
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 20
    else:
        suggestions.append("Make the password at least 12 characters long.")

    # Character variety
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any((not c.isalnum()) for c in password)

    variety = sum([has_lower, has_upper, has_digit, has_symbol])
    score += variety * 15
    if not has_lower:
        suggestions.append("Add lowercase letters.")
    if not has_upper:
        suggestions.append("Add uppercase letters.")
    if not has_digit:
        suggestions.append("Include digits.")
    if not has_symbol:
        suggestions.append("Include symbols or punctuation.")

    # Simple entropy boost for length and variety
    if length >= 20 and variety == 4:
        score = min(100, score + 10)

    # Normalize score to 0-100
    score = max(0, min(100, score))

    if score >= 80:
        rating = "Strong"
    elif score >= 50:
        rating = "Medium"
    else:
        rating = "Weak"

    return {"score": score, "rating": rating, "suggestions": suggestions}


def check_password_strength(password: str) -> str:
    result = check_strength(password)
    return f"{result['rating']} ({result['score']}%)"


