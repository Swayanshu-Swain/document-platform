import boto3
import os

session = boto3.Session()

AWS_REGION = os.getenv(
    "AWS_REGION"
)

FLASK_SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY"
)

DYNAMODB_USERS_TABLE = os.getenv(
    "DYNAMODB_USERS_TABLE"
)

AWS_S3_BUCKET = os.getenv(
    "AWS_S3_BUCKET"
)
