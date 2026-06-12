import bcrypt

from services.dynamodb_service import (
    get_user,
    get_all_users
)


def authenticate_user(
    username,
    password
):

    user = get_user(username)

    if not user:
        return None

    if not user.get("active"):
        return None

    stored_hash = user["password"]

    if bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    ):
        return user

    return None

def get_shareable_users(
    file,
    users
):

    result = []

    for user in users:

        username = user["username"]

        if (
            user["role"]
            == file["department"]
        ):
            continue

        if (
            username
            in file["shared_with"]
        ):
            continue

        result.append(user)

    return result

