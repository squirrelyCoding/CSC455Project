import string
import secrets

def generate_password(length: int = 16):
    if (length < 12):
        raise ValueError("Your password must be at least 12 characters long.")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    print(password)
    return password

print("Generated password: " + generate_password())

def check_password_strength(password: str) -> str:
    length = len(password)
    if length < 12:
        
        return "Password strength is poor. Length must be at least 12 characters."
    elif length < 16:
        return "Password strength is okay. Consider making your password at least 16 characters."
    else:
        return "Password strength is really strong!"