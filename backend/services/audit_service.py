import boto3

from datetime import datetime

from config.settings import (
    AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

audit_table = dynamodb.Table(
    "audit_logs"
)


def log_event(

    username,

    action,

    file_id,

    file_name,

    department,

    details
):

    timestamp = (
        datetime.utcnow()
        .isoformat()
    )

    audit_table.put_item(

        Item={

            "username":
                username,

            "timestamp":
                timestamp,

            "action":
                action,

            "file_id":
                file_id,

            "file_name":
                file_name,

            "department":
                department,

            "details":
                details
        }
    )
