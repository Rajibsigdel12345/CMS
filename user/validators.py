import re

def EmailValidator(value):
    if not value:
        return 'Email is required'
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        return 'Email is invalid'
    return None