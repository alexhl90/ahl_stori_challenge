import json
import os
from datetime import date as dt, datetime

from typing import Dict, List
import base64

from src.upload.utils import upload_file_to_s3

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

def parse_and_upload(event) -> Dict:
    body = json.loads(event.get("body"))
    doc_b64 = body.get("doc_b64")
    plain_csv = base64.b64decode(doc_b64.split(",")[1])
    csv_file_path = "/tmp/tmp_file.csv"
    with open(csv_file_path, "wb") as csv_file:
        csv_file.write(plain_csv)
    upload_file_to_s3(S3_BUCKET_NAME, f"{datetime.now().timestamp()}.csv", csv_file_path)
    os.remove(csv_file_path)
    return {
        "status_code": 200,
    }

def handler(event: Dict, context):
    print(f"Received event: {event.keys()}")
    return parse_and_upload(event)