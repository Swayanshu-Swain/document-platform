from datetime import datetime

from services.dynamodb_service import dynamodb

from boto3.dynamodb.conditions import Key

from config.settings import (
    DYNAMODB_FILES_TABLE
)

files_table = dynamodb.Table(
    DYNAMODB_FILES_TABLE
)

def create_file_metadata(
    file_id,
    filename,
    department,
    uploaded_by,
    s3_key,
    file_size,
    content_type
):

    item = {

        "file_id": file_id,

        "display_name": filename,

        "department": department,

        "uploaded_by": uploaded_by,

        "uploaded_at":
            datetime.utcnow().isoformat(),

        "status": "ACTIVE",

        "s3_key": s3_key,

        "file_size": file_size,

        "content_type": content_type,

        "shared_with": []
    }

    files_table.put_item(
        Item=item
    )

    return item
def get_owned_files(
    username
):

    response = files_table.scan()

    result = []

    for file in response["Items"]:

        if (
            file["uploaded_by"]
            == username
            and
            file["status"]
            == "ACTIVE"
        ):

            result.append(file)

    return result
def get_shared_files(
    username
):

    response = files_table.scan()

    result = []

    for file in response["Items"]:

        if (

            username in file.get(
                "shared_with",
                []
            )

            and

            file["status"]
            == "ACTIVE"
        ):

            result.append(file)

    return result
def get_files_by_department(
    department
):

    response = files_table.query(

        IndexName="department-index",

        KeyConditionExpression=
            Key("department").eq(
                department
            ),

        ScanIndexForward=False

    )

    return response["Items"]
def get_file_by_id(
    file_id
):

    response = files_table.get_item(
        Key={
            "file_id": file_id
        }
    )

    return response.get(
        "Item"
    )
def share_file(
    file_id,
    username
):

    file = get_file_by_id(
        file_id
    )

    shared_with = file.get(
        "shared_with",
        []
    )

    if username not in shared_with:

        shared_with.append(
            username
        )

        files_table.update_item(

            Key={
                "file_id": file_id
            },

            UpdateExpression=
                "SET shared_with = :s",

            ExpressionAttributeValues={
                ":s": shared_with
            }
        )
def get_files_shared_with_user(
    username
):

    response = files_table.scan()

    result = []

    for file in response["Items"]:

        if username in file.get(
            "shared_with",
            []
        ):
            result.append(file)

    return result
def soft_delete_file(
    file_id,
    deleted_by
):

    files_table.update_item(

        Key={
            "file_id": file_id
        },

        UpdateExpression=
        """
        SET
            #s = :status,
            deleted_by = :deleted_by,
            deleted_at = :deleted_at
        """,

        ExpressionAttributeNames={
            "#s": "status"
        },

        ExpressionAttributeValues={

            ":status":
                "DELETED",

            ":deleted_by":
                deleted_by,

            ":deleted_at":
                datetime.utcnow().isoformat()
        }
    )
def remove_shared_access(
    file_id,
    username
):

    file = get_file_by_id(
        file_id
    )

    shared_with = file.get(
        "shared_with",
        []
    )

    if username in shared_with:

        shared_with.remove(
            username
        )

        files_table.update_item(

            Key={
                "file_id": file_id
            },

            UpdateExpression=
                "SET shared_with = :s",

            ExpressionAttributeValues={
                ":s": shared_with
            }
        )
def get_deleted_files(
    username
):

    response = files_table.scan()

    result = []

    for file in response["Items"]:

        if (

            file.get(
                "uploaded_by"
            ) == username

            and

            file.get(
                "status"
            ) == "DELETED"
        ):

            result.append(
                file
            )

    return result
def restore_file(
    file_id
):

    files_table.update_item(

        Key={
            "file_id": file_id
        },
        UpdateExpression=
        """
        SET #s = :status
        """,
        ExpressionAttributeNames={
            "#s": "status"
        },
        ExpressionAttributeValues={
            ":status":"ACTIVE"
        }
    )
def get_total_documents():

    response = files_table.scan()

    return len(
        response["Items"]
    )


def get_total_shared():

    response = files_table.scan()

    count = 0

    for item in response["Items"]:

        if len(
            item.get(
                "shared_with",
                []
            )
        ) > 0:

            count += 1

    return count