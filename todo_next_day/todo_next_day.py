from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

load_dotenv()

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
TIME_ZONE = "Asia/Tashkent"


def get_first_weekday():
    today = datetime.now(ZoneInfo(TIME_ZONE))
    return today - timedelta(days=today.weekday())


def adjust_to_current_week(date):
    page_current_date = get_first_weekday() + timedelta(days=date.weekday())
    return page_current_date.replace(
        hour=date.hour, minute=date.minute, second=0, microsecond=0
    )


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

        page_add_response = requests.post(
            "https://api.notion.com/v1/pages", headers=HEADER, json=page
        )
        if page_add_response.status_code != 200:
            print(response.json())


HEADER = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

CURRENT_DAY = datetime.now(ZoneInfo(TIME_ZONE)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
PREVIOUS_DAY = CURRENT_DAY - timedelta(days=1)

query_body = {
    "filter": {
        "and": [
            {
                "and": [
                    {
                        "property": "Date",
                        "date": {"on_or_after": PREVIOUS_DAY.isoformat()},
                    },
                    {
                        "property": "Date",
                        "date": {"before": CURRENT_DAY.isoformat()},
                    },
                ]
            },
            {
                "or": [
                    {"property": "Recurrence", "select": {"equals": "Todo"}},
                    {
                        "property": "Recurrence",
                        "select": {"equals": "Weekly"},
                    },
                ]
            },
            {"property": "Completion", "checkbox": {"equals": False}},
        ]
    },
    "sorts": [{"property": "Date", "direction": "ascending"}],
}
response = requests.post(
    f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
    headers=HEADER,
    json=query_body,
)
if response.status_code != 200:
    print(response.status_code)
    print(response.json())
    quit()


pages = response.json()["results"]
for page in pages:
    patch_body = {
        "properties": {
            "Date": {
                "type": "date",
                "date": {"start": CURRENT_DAY.strftime("%Y-%m-%d")},
            }
        }
    }
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page['id']}",
        headers=HEADER,
        json=patch_body,
    )
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        quit()

print(f"Moved {len(pages)} tasks to current day")
