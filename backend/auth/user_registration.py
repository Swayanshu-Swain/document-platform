import bcrypt

from services.dynamodb_service import (
    get_user,
    create_user
)


def register_user(
    username,
    password,
    role
):
    existing_user = get_user(username)

    if existing_user:
        return False, "Username already exists"

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = {
        "username": username,
        "password": hashed_password,
        "role": role,
        "active": True
    }

    create_user(user)

    return True, "User created successfully"
