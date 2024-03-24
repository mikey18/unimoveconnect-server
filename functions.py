import bcrypt

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password: str, hash_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hash_password)
