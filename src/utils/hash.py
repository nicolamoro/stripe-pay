from hashlib import pbkdf2_hmac


def generate_hash(plaintext):
    hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plaintext, "utf-8"),
        b"",
        10000,
    )
    return hash.hex()
