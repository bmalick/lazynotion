import yaml
from typing import Dict

def headers() -> Dict[str,str]:
    with open("keys.yml", "r") as f:
        api_key = yaml.safe_load(f)["notion_api_key"]

    return {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer %s" % api_key
    }

