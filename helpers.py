import bcrypt

def check_password_hash(stored_hash, provided_password):
    stored_hash_bytes = stored_hash.encode('utf-8')
    provided_password_bytes = provided_password.encode('utf-8')

    return bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)

