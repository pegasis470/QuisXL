import os
import string
import random 
import bcrypt


AUTH_KEY=os.getenv("AUTH_KEY_GEN","default")


def hash_password(password: str) -> str:
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')


def genrate_auth_token(auth_key: str):
    if AUTH_KEY != auth_key:
        raise ValueError("AUTH_KEY_ERROR")
    else:
        letters = string.ascii_letters  # Includes both uppercase and lowercase letters
        random_string = ''.join(random.choice(letters) for _ in range(4))
        auth_token=hash_password(random_string)
        return auth_token