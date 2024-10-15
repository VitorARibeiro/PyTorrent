import hashlib


def hash_sha1(data):
    """
    Compute SHA-1 hash of the input data.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')  # Convert string to bytes

    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    hashed_value = sha1_hash.digest()

    return hashed_value
