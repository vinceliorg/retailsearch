import hashlib

def encode(text):
    hash_object = hashlib.md5(text.encode('utf-8'))
    return hash_object.hexdigest()
