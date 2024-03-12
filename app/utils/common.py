from bson import ObjectId
import re

def objectid_to_string(value: ObjectId) -> str:
    """Convert ObjectId to string."""
    return str(value)

def is_valid_email(email: str) -> bool:
    """Check if the provided string is a valid email address."""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None
