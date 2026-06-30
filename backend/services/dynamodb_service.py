import boto3
import bcrypt

from config.settings import (
    AWS_REGION,
    DYNAMODB_USERS_TABLE,
    DYNAMODB_AUDIT_TABLE
)


def get_users_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION
    )

    return dynamodb.Table(
        DYNAMODB_USERS_TABLE
    )

def get_audit_table():

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION
    )

    return dynamodb.Table(
        DYNAMODB_AUDIT_TABLE
    )

def get_user(username):
    users_table=get_users_table()
    response = users_table.get_item(
        Key={
            "username": username
        }
    )

    return response.get("Item")

def get_all_users():

    users_table=get_users_table()
    response = users_table.scan()

    return response["Items"]

def create_user(user_data):

    users_table=get_users_table()
    users_table.put_item(
        Item=user_data
    )

def disable_user(username):

    users_table=get_users_table()
    users_table.update_item(
        Key={
            "username": username
        },
        UpdateExpression=
            "SET active = :a",
        ExpressionAttributeValues={
            ":a": False
        }
    )

def enable_user(username):

    users_table=get_users_table()
    users_table.update_item(
        Key={
            "username": username
        },
        UpdateExpression=
            "SET active = :a",
        ExpressionAttributeValues={
            ":a": True
        }
    )

def reset_password(
    username,
    password
):

    password_hash = (
        bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()
    )

    users_table=get_users_table()
    users_table.update_item(
        Key={
            "username": username
        },
        UpdateExpression=
            "SET password = :p",
        ExpressionAttributeValues={
            ":p": password_hash
        }
    )
def get_audit_logs():
    audit_table=get_audit_table()
    response = audit_table.scan()

    items = response["Items"]

    items.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return items
