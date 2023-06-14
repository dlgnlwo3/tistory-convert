import re

def is_email_valid(email):
    REGEX_EMAIL = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if not re.fullmatch(REGEX_EMAIL, email):
        return False
    
    return True