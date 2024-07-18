import json
import os
import smtplib
from datetime import date as dt
from typing import Dict, List

from src.mail_send.utils import build_email_content, build_smtp_msg

SENDER_MAIL = os.environ.get("SENDER_EMAIL", "from@example.com")
USE_TLS = int(os.environ.get("USE_TLS", 0))
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 0))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_USER_PASSWORD = os.environ.get("SMTP_USER_PASSWORD", "")


def build_and_send_email(body):
    user_email = body.get("user_email")
    email_content = build_email_content(body)
    if not email_content:
        return {"statusCode": 500, "body": json.dumps("Error building email content.")}
    smtp_msg = build_smtp_msg(SENDER_MAIL, user_email, email_content)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if USE_TLS:
            server.starttls()
        server.login(SMTP_USER, SMTP_USER_PASSWORD)
        server.sendmail(SENDER_MAIL, user_email, smtp_msg)
    return {
        "statusCode": 200,
        "body": json.dumps(f"Email sent successfully to {user_email}!"),
    }


def handler(event, context):
    return build_and_send_email(event)
