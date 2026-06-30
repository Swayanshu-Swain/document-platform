import boto3
import bcrypt

from config.settings import (
    AWS_REGION,
    DYNAMODB_USERS_TABLE,
    DYNAMODB_FILES_TABLE,
    DYNAMODB_AUDIT_TABLE,
)


def get_dynamodb():
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
    )


def get_users_table():
    return get_dynamodb().Table(
        DYNAMODB_USERS_TABLE
    )


def get_files_table():
    return get_dynamodb().Table(
        DYNAMODB_FILES_TABLE
    )


def get_audit_table():
    return get_dynamodb().Table(
        DYNAMODB_AUDIT_TABLE
    )


def get_user(username):

    response = get_users_table().get_item(
        Key={
            "username": username
        }
    )

    return response.get("Item")


def get_all_users():

    response = get_users_table().scan()

    return response["Items"]


def create_user(user_data):

    get_users_table().put_item(
        Item=user_data
    )


def disable_user(username):

    get_users_table().update_item(
        Key={
            "username": username
        },
        UpdateExpression="SET active = :a",
        ExpressionAttributeValues={
            ":a": False
        }
    )


def enable_user(username):

    get_users_table().update_item(
        Key={
            "username": username
        },
        UpdateExpression="SET active = :a",
        ExpressionAttributeValues={
            ":a": True
        }
    )


def reset_password(username, password):

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    get_users_table().update_item(
        Key={
            "username": username
        },
        UpdateExpression="SET password = :p",
        ExpressionAttributeValues={
            ":p": password_hash
        }
    )


def get_audit_logs():

    response = get_audit_table().scan()

    items = response["Items"]

    items.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return items
