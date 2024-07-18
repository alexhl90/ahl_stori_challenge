import boto3


def download_file_from_s3(bucket_name, object_key, file_name):
    client = boto3.client("s3")
    client.download_file(bucket_name, object_key, file_name)
