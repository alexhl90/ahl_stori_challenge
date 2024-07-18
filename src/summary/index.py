from typing import List, Dict
from datetime import datetime, date as dt
import json
import boto3
import os
from src.summary.utils import download_file_from_s3, invoke_lambda

MAIL_LAMBDA = os.environ.get("MAIL_LAMBDA")
STORE_LAMBDA = os.environ.get("STORE_LAMBDA")


## invoke lambda to send email via boto3


##process and analyze data
def process_txn(transactions: List[List]) -> Dict:
    total_balance = 0
    total_amount_credit_transactions = 0
    total_amount_debit_transactions = 0
    credit_txn_count = 0
    debit_txn_count = 0

    transactions_by_month = {}

    for transaction in transactions:
        id_txn, date, transaction_str = transaction
        transaction_amount = float(transaction_str.replace("+", ""))
        total_balance += transaction_amount
        if transaction_amount > 0:
            total_amount_credit_transactions += transaction_amount
            credit_txn_count += 1
        else:
            total_amount_debit_transactions += transaction_amount
            debit_txn_count += 1
        formatted_date = datetime.strptime(date, "%Y/%m/%d")
        month = formatted_date.strftime("%m")
        month_text = formatted_date.strftime("%B")
        txn_info = {
            "date": date,
            "transaction_amount": transaction_amount,
            "id": id_txn,
        }
        if month in transactions_by_month:
            transactions_by_month[month].get("transactions").append(txn_info)
        else:
            transactions_by_month[month] = {
                "name": month_text,
                "transactions": [txn_info],
            }
        # balance for each month
        for month, data in transactions_by_month.items():
            txn_amounts = [txn["transaction_amount"] for txn in data["transactions"]]
            m_credit_txn = [
                txn["transaction_amount"] > 0 for txn in data["transactions"]
            ]
            m_debit_txn = [
                txn["transaction_amount"] < 0 for txn in data["transactions"]
            ]
            data["balance"] = round(sum(txn_amounts), 2)
            data["avg_credit"] = (
                round(sum(m_credit_txn) / len(m_credit_txn), 2)
                if len(m_credit_txn) > 0
                else 0
            )
            data["avg_debit"] = (
                round(sum(m_debit_txn) / len(m_debit_txn), 2)
                if len(m_debit_txn) > 0
                else 0
            )

    return {
        "total_balance": total_balance,
        "total_amount_credit_transactions": total_amount_credit_transactions,
        "total_amount_debit_transactions": total_amount_debit_transactions,
        "avg_credit_txn": round(total_amount_credit_transactions / credit_txn_count, 2),
        "avg_debit_txn_count": round(
            total_amount_debit_transactions / debit_txn_count, 2
        ),
        "transactions_by_month": transactions_by_month,
    }


## read file and print data
def process_file(file_path):
    try:
        transactions = []
        email = ""
        with open(file_path, "r") as file:
            skip_first_2 = 0
            for line in file:
                if skip_first_2 < 2:
                    if line.startswith("user_email"):
                        email = line.split(":")[1].strip()
                    skip_first_2 += 1
                    continue
                transactions.append(line.strip().split(","))
        if transactions:
            summary = process_txn(transactions)
            payload = {
                "user_email": email,
                "summary": summary,
            }
            invoke_lambda(MAIL_LAMBDA, payload)
            invoke_lambda(STORE_LAMBDA, payload)
            return {
                "statusCode": 200,
                "body": "Data read successfully.",
            }
        else:
            print(f"No transactions found in {file_path} for user {email}.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return {"statusCode": 500, "body": json.dumps("Error saving data to file.")}
    return {
        "statusCode": 200,
        "body": "Data read successfully.",
    }


def handler(event, context):
    if event.get("Records", []):
        for record in event.get("Records"):
            s3_event = record.get("s3")
            if s3_event:
                bucket_name = s3_event.get("bucket").get("name")
                object_key = s3_event.get("object").get("key")
                print(f"Processing {bucket_name}/{object_key}")
                file_path = "/tmp/transactions.csv"
                download_file_from_s3(bucket_name, object_key, file_path)
                return process_file(file_path)
    else:
        return process_file("/shared_data/transactions.csv")
