from typing import Dict
import os
def get_template() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content



def handler(event, context):
    content_html = get_template()
    return {
        "statusCode": 200,
        "body": content_html,
        "headers": {"Content-Type": "text/html"},  # Set the response content type as HTML.
    }