import requests
from typing import Dict, List, Tuple

from src.lazynotion import blocks
from src.lazynotion import auth
from src.lazynotion import page
from src.lazynotion import logs
from src.lazynotion import icons

SEARCH_ENDPOINT = "https://api.notion.com/v1/search"

def search_all(search_params: Dict = {}):
    
    # logger = logs.get_logger()

    headers = auth.headers()

    response = requests.post(
        url=SEARCH_ENDPOINT,
        headers=headers,
        json=search_params
    )
    try:
        response.raise_for_status()
        out = response.json()
        return out["results"]
    except:
        print(response.text)

def search_databases(db_name: str):
    return search_all({"query": db_name, "filter": {"value": "database", "property": "object"}})

def search_pages():
    pass
