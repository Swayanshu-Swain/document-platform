import boto3

from datetime import datetime

from config.settings import (
    AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

from config.settings import (
    DYNAMODB_AUDIT_TABLE
)

audit_table = dynamodb.Table(
    DYNAMODB_AUDIT_TABLE
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
def get_total_audit_events():

    response = audit_table.scan()

    return len(
        response["Items"]
    )
def get_recent_audit_events():

    response = audit_table.scan()

    items = response.get(
        "Items",
        []
    )

    items.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return items[:10]