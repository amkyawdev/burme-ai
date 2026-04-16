"""
Security Module
Handles authentication and security utilities
"""
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks"""
    # Basic sanitization - remove potentially dangerous characters
    dangerous_chars = ["<", ">", "&", '"', "'", ";", "--", "/*", "*/"]
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    return sanitized.strip()


def rate_limit_key(client_ip: str, endpoint: str) -> str:
    """Generate rate limit key for a client"""
    return f"rate_limit:{client_ip}:{endpoint}"