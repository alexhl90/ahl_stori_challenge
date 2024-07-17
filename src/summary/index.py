from typing import List, Dict
from datetime import datetime, date as dt
import json
import boto3

## invoke lambda to send email via boto3
def invoke_send_email(body: Dict) -> None:
    client = boto3.client('lambda')
    return {
        "statusCode": 200,
        "body": json.dumps("Email Queued!")
    }

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
        txn_info = {
            "date": date,
            "transaction_amount": transaction_amount,
            "id": id_txn,
        }
        if month in transactions_by_month:
            transactions_by_month[month].append(txn_info)
        else:
            transactions_by_month[month] = [txn_info]
    return {
        "total_balance": total_balance,
        "total_amount_credit_transactions": total_amount_credit_transactions,
        "total_amount_debit_transactions": total_amount_debit_transactions,
        "credit_txn_count": credit_txn_count,
        "debit_txn_count": debit_txn_count,
        "transactions_by_month": transactions_by_month,
    }


## read file and print data
def read_file(file_path):
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
            return invoke_send_email({
                email: email,
                "summary": summary,
            })
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
    return read_file("/shared_data/transactions.csv")
