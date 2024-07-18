import json
import os
import boto3

STAGE = os.environ.get("STAGE", "local")


def invoke_lambda(lambda_name, body) -> None:
    payload_client = {}
    if STAGE == "local":
        payload_client = {"endpoint_url": "http://localhost:3002"}
    lambda_client = boto3.client("lambda", **payload_client)
    print(f"Invoke Lambda: {lambda_name}")
    lambda_client.invoke(
        FunctionName=lambda_name,
        Payload=(json.dumps(body)),
    )
