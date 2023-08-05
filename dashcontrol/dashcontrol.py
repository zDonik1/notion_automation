from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from flask import Flask
from flask import redirect, abort

load_dotenv()
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

HEADER = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

app = Flask("dashcontrol")

@app.route("/addtodo")
def index():
    page = {
        "parent": {"database_id": DATABASE_ID},
        "icon": {
            "type": "external",
            "external": {"url": "https://www.notion.so/icons/checkmark_green.svg"},
        },
        "properties": {
            "Date": {
                "type": "date",
                "date": {"start": datetime.now().strftime("%Y-%m-%d")},
            },
            "Recurrence": {
                "type": "select",
                "select": {"name": "Once", "color": "green"},
            }
        }
    }
    response = requests.post("https://api.notion.com/v1/pages", headers=HEADER, json=page)
    if response.status_code != 200:
        print(response.json())
        abort()

    return redirect(response.json()["url"])