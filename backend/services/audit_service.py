from datetime import datetime

from services.dynamodb_service import (
    get_audit_table
)


def log_event(
    username,
    action,
    file_id,
    file_name,
    department,
    details
):

    audit_table = get_audit_table()

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

    audit_table = get_audit_table()

    response = audit_table.scan()

    return len(
        response["Items"]
    )


def get_recent_audit_events():

    audit_table = get_audit_table()

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
