import boto3

from config.settings import (
    AWS_REGION,
    DYNAMODB_USERS_TABLE
)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

users_table = dynamodb.Table(
    DYNAMODB_USERS_TABLE
)


def get_user(username):
    response = users_table.get_item(
        Key={
            "username": username
        }
    )

    return response.get("Item")
def get_all_users():

    response = users_table.scan()

    return response["Items"]
