import hashlib
import os
import hmac


def hash_password(password: str) -> str:
  salt = os.urandom(16)  
  derived_key = hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt, 100_000
  )
  return f"{salt.hex()}:{derived_key.hex()}"


def verify_password(stored_password: str, provided_password: str) -> bool:
  try:
    salt_hex, original_hash_hex = stored_password.split(":")
    salt = bytes.fromhex(salt_hex)
    original_hash = bytes.fromhex(original_hash_hex)
    new_hash = hashlib.pbkdf2_hmac(
        "sha256", provided_password.encode("utf-8"), salt, 100_000
    )

    return hmac.compare_digest(original_hash, new_hash)
  except ValueError:
    return False
