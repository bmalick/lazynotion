import os
from typing import Dict

def headers() -> Dict[str,str]:
    api_key = os.environ["NOTION_API_KEY"]
    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer %s" % api_key
    }

if __name__ == "__main__":
    print(headers())
