import boto3


def download_file_from_s3(bucket_name, object_key, file_name):
    client = boto3.client("s3")
    client.download_file(bucket_name, object_key, file_name)



def upload_file_to_s3(bucket_name, object_key, file_name):
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket_name, object_key)