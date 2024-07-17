from typing import List, Dict
from datetime import datetime, date as dt
import json





def handler(event, context):
    print(f"Event: {event}")
    return {
        "statusCode": 200,
        "body": json.dumps("Send mail!")
    }
