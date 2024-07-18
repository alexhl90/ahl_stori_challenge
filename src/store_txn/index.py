from typing import List, Dict
from datetime import date as dt
import boto3
import os
from uuid import uuid4

TABLE_NAME = os.environ.get("TABLE_NAME")


def store_txn(body: Dict[str, any]):
    user_id = body.get("user_email")
    summary = body.get("summary")
    txn_by_month = summary.get("transactions_by_month")
    whole_txn = []
    for _, month_data in txn_by_month.items():
        for txn_info in month_data["transactions"]:
            id_txn = str(uuid4())
            transaction_amount = float(txn_info.get("transaction_amount"))
            date = txn_info.get("date")
            txn_type = "credit" if transaction_amount > 0 else "debit"
            whole_txn.append(
                {
                    "PutRequest": {
                        "Item": {
                            "user_id": {"S": user_id},
                            "txn_id": {"S": id_txn},
                            "transaction_amount": {"N": f"{transaction_amount:+.2f}"},
                            "date": {"S": date},
                            "txn_type": {"S": txn_type},
                        }
                    }
                }
            )
    try:
        client = boto3.client("dynamodb")
        slice_size = 20
        while whole_txn:
            items_to_write = whole_txn[:slice_size]
            print(f"Storing {len(items_to_write)} transactions for user {user_id}.")
            print(whole_txn[0])
            whole_txn = whole_txn[slice_size:]
            response = client.batch_write_item(
                RequestItems={
                    f"{TABLE_NAME}": items_to_write,
                }
            )
            print(f"Storing {response} transactions for user {user_id}.")

        return {
            "status_code": 200,
        }
    except Exception as e:
        print(f"Error storing transaction data: {str(e)}")
        return {
            "status_code": 500,
        }


def handler(event, context):
    return store_txn(event)
