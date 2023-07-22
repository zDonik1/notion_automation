from dotenv import load_dotenv
import os
import requests

load_dotenv()

DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
WEEK_DB_ID = os.getenv('NOTION_WEEK_DB_ID')


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
            "property": "Date", 
            "date": {
                "equals": f"2023-07-{START_DAY + i}"
            }
        }
    }
    response = requests.post(f'https://api.notion.com/v1/databases/{WEEK_DB_ID}/query', headers=header, json=query_body)
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        break
    
    response_dict = response.json()
    upload_pages(response_dict["results"])
    print(f"Uploaded {len(response_dict['results'])} pages")