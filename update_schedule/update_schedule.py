from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta

NAME_FILTER = "retrospect day"
TIMES = [
    "21:00",
    "21:00",
    "21:00",
    "21:00",
    "21:00",
    "21:00",
    "21:00",
]
DELTA = 0

load_dotenv()

DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S+05:00"

HEADER = {
    "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

query_body = {
    "filter": {
        "and": [
            {
                "property": "Date",
                "date": {"on_or_after": f"2023-07-17T00:00:00+05:00"},
            },
            {
                "property": "Date",
                "date": {"before": f"2023-07-24T00:00:00+05:00"},
            },
            {
                "property": "Name",
                "rich_text": {"contains": NAME_FILTER},
            },
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
for page, time in zip(pages, TIMES):
    date_obj = page["properties"]["Date"]["date"]
    start = datetime.fromisoformat(date_obj["start"])

    str_hour, str_minute = time.split(":")
    start = start.replace(hour=int(str_hour), minute=int(str_minute))

    end = None
    if DELTA != 0:
        end = start + timedelta(minutes=DELTA)

    date_obj = {"start": start.strftime(DATE_FORMAT)}
    if end is not None:
        date_obj["end"] = end.strftime(DATE_FORMAT)

    patch_body = {
        "properties": {
            "Date": {
                "type": "date",
                "date": date_obj,
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

print(f"Updated {len(pages)} pages")