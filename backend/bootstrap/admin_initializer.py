import bcrypt

from services.dynamodb_service import (
    get_user,
    create_user
)


def initialize_admin():

    admin = get_user("admin")

    if admin:
        print(
            "Admin user already exists"
        )
        return

    password_hash = bcrypt.hashpw(
        "admin123".encode(),
        bcrypt.gensalt()
    ).decode()

    create_user({
        "username": "admin",
        "password": password_hash,
        "role": "admin",
        "active": True
    })

    print(
        "Admin user created"
    )
