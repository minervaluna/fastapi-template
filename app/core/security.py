# app/core/security.py
import bcrypt


def get_password_hash(password: str) -> str:
    """
    using bcrypt.hashpw to generate hashed password.
    params：
      - password: origin password
    return：
      - hash result
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    using bcrypt.checkpw to verify if the input password is correct.
    """
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
