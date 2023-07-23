from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

load_dotenv()

DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
WEEK_DB_ID = os.getenv('NOTION_WEEK_DB_ID')
TIME_ZONE = "Asia/Tashkent"


def get_first_weekday():
    today = datetime.now(ZoneInfo(TIME_ZONE))
    return today - timedelta(days=today.weekday())


def adjust_to_current_week(date):
    page_current_date = get_first_weekday() + timedelta(days=date.weekday())
    return page_current_date.replace(hour=date.hour, minute=date.minute, second=0, microsecond=0)


def get_date_in_page(page):
    return page["properties"]["Date"]["date"]


def get_adjusted_date_in_page(page, component):
    date_str = get_date_in_page(page)[component]
    if not date_str:
        return None
    return adjust_to_current_week(datetime.fromisoformat(date_str))


def adjust_page_date(page, component):
    date = get_adjusted_date_in_page(page, component)
    if date is not None:
        get_date_in_page(page)[component] = date.isoformat()


def edit_date_on_pages(pages):
    for page in pages:
        adjust_page_date(page, "start")
        adjust_page_date(page, "end")


def upload_pages(pages):
    for page in pages:
        page["parent"]["database_id"] = DATABASE_ID

        page_add_response = requests.post('https://api.notion.com/v1/pages', headers=header, json=page)
        if page_add_response.status_code != 200:
            print(response.json())


header = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

START_DAY = 17
for i in range(7):
    query_body = {
        "filter": {
            "and": [
                {
                    "property": "Date", 
                    "date": {
                        "on_or_after": f"2023-07-{START_DAY + i}T00:00:00+05:00"
                    }
                },
                {
                    "property": "Date", 
                    "date": {
                        "before": f"2023-07-{START_DAY + i}T23:59:59+05:00"
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "ascending"
            }
        ]
    }
    response = requests.post(f'https://api.notion.com/v1/databases/{WEEK_DB_ID}/query', headers=header, json=query_body)
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        break
    
    pages = response.json()["results"]
    edit_date_on_pages(pages)
    upload_pages(pages)
    print(f"Uploaded {len(pages)} pages")