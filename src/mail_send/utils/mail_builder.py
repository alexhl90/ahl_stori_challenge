from typing import Dict
import os
import json
from datetime import date as dt
def replace_tags(template_name, variables: Dict[str, str]) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, '..', 'templates', f'{template_name}.html')
    
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    for key, value in variables.items():
        html_content = html_content.replace(f"!!{key}", str(value))

    return html_content
def build_email_content(body: Dict[str, any]) -> str:
    fake_name = body.get("user_email").split("@")[0]
    summary = body.get("summary")

    try:
        total_balance = summary.get("total_balance")
        avg_debit_txn_count = summary.get("avg_debit_txn_count")
        avg_credit_txn = summary.get("avg_credit_txn")
        transactions_by_month = summary.get("transactions_by_month")
        monthly_html_part = ""
        for _, month_data in transactions_by_month.items():
            variables = {
                "MONTH": month_data.get("name"),
                "BALANCE": f"${month_data.get('balance'):.2f}",
                "NUMBER": len(month_data.get("transactions")),
                "AVG_DEBIT": f"${month_data.get('avg_debit'):.2f}",
                "AVG_CREDIT": f"${month_data.get('avg_credit'):.2f}",
            }
            monthly_html_part += replace_tags("monthly", variables)
        body_variables = {
            "NAME": fake_name,
            "TOTAL_BALANCE": f"${total_balance:.2f}",
            "CREDIT_AMOUNT": f"${avg_credit_txn:.2f}",
            "DEBIT_AMOUNT": f"${avg_debit_txn_count:.2f}",
            "MONTHLY_DATA": monthly_html_part,
            "DATE": dt.today().strftime("%B %d, %Y"),
        }
        html_content = replace_tags("body", body_variables)
        html_content = html_content.replace(u'\xa0', u' ')
    except Exception as e:
        print(f"Error building email content: {str(e)}")
        return False
    return html_content

def build_smtp_msg(
    sender: str, receiver: str, html_content: str, subject: str = "Movements summary!", sender_nickname: str = "Stori Challenge"
)-> str:
    from_statement = f"From: {sender_nickname} <{sender}>"
    to_statement = f"To:{receiver.split('@')[0]} <{receiver}>"
    message = f"""\
{to_statement}
{from_statement}
Subject: {subject}
Content-Type: multipart/alternative; boundary="boundary-string"

--boundary-string
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline

{html_content}

--boundary-string--"""
    return message