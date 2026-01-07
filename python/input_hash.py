import hashlib

def generate_sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest().upper()

print(generate_sha256_hash('3edc@YHN'))