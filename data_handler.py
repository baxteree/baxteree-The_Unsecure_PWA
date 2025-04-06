import re
import html


# Simple password checking function
def checkpw(password: str) -> bool:
    if not issubclass(type(password), str):
        return False
    if len(password) < 8:
        return False
    if len(password) > 20:
        return False
    if re.search(r"[ ]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return True


# A more complex check password function including errors
def checkpw_2(password: str) -> bytes:
    if not issubclass(type(password), str):
        raise TypeError("Expected a string")
    if len(password) < 8:
        raise ValueError("has less than 8 characters")
    if len(password) > 20:
        raise ValueError("has more than 20 characters")
    if re.search(r"[ ]", password):
        raise ValueError("contains ' ' space characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("contains no uppercase letters")
    if not re.search(r"[a-z]", password):
        raise ValueError("contains no lowercase letters")
    if not re.search(r"[0-9]", password):
        raise ValueError("does not contain a digit '0123456789'")
    if not re.search(r"[@$!%*?&]", password):
        raise ValueError("does not contain one of '@$!%*?&' special characters")
    # Password is returned encoded so it can't be accidently logged in a human readable format
    return password

# Function to sanitise text using a library
def make_web_safe(string: str) -> str:
    return html.escape(string)
