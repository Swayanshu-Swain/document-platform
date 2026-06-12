import boto3

from config.settings import (
    AWS_REGION,
    AWS_S3_BUCKET
)

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)

def upload_file_to_s3(
    file,
    s3_key
):

    s3_client.upload_fileobj(

        file,

        AWS_S3_BUCKET,

        s3_key,

        ExtraArgs={
            "ContentType":
                file.content_type
        }
    )

def generate_presigned_url(
    s3_key
):

    url = s3_client.generate_presigned_url(

        "get_object",

        Params={
            "Bucket": AWS_S3_BUCKET,
            "Key": s3_key
        },

        ExpiresIn=300
    )

    return url
