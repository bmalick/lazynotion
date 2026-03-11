import os
import requests
from typing import Dict, List, Tuple

from src.lazynotion import blocks
from src.lazynotion import auth
from src.lazynotion import page
from src.lazynotion import logs
from src.lazynotion import icons
from src.lazynotion import search
from src.lazynotion import utils

class Database:
    endpoint = "https://api.notion.com/v1/databases"
    update_endpoint = "https://api.notion.com/v1/databases/%s"
    query_endpoint = ""
    retrieve_endpoint = ""

    def __init__(self, db_id: str = None, parent_id: str = None, logger = None):
        self.db_id = db_id
        self.parent_id = parent_id
        self.headers = auth.headers()
        self.logger = logger
        self.properties = None
        self.title = None
        self.url = None
        self.notion_account = utils.get_account_name()

    def __str__(self):
        return f"Database(title={self.title}, id={self.db_id}, parent={self.parent_id}, url={self.url})"

    def log(self, message: str):
        if self.logger is None:
            print(f"[Notion account={self.notion_account}] [Database] " + message)
        else:
            self.logger.info(f"[Notion account={self.notion_account}] [Database] " + message)


    def create(self,
            db_title: str,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = {}
        ) -> Dict:
        assert self.parent_id is not None, "You must specify a page/database parent id"
        searched_dbs = search.search_databases(db_title)
        out = None
        for res in searched_dbs:
            if res["title"][0]["text"]["content"] == db_title:
                out = res
        if out is not None:
            self.db_id = out["id"]
            self.title = db_title
            self.url = out["url"]
            self.properties = list(out["properties"].keys())
            self.log(f"Already created: {self}")
            return out

        parent = blocks.PageParent(self.parent_id)
        icon = blocks.Icon(emoji=icon_emoji,url=icon_url)
        cover = blocks.Cover(url=cover_url)
        title_item = blocks.PageTitle(title=db_title)

        properties_data = {"Name": {"title": {}}}
        for p in properties:
            properties_data.update(p.init_data)
        response = requests.post(
            url=self.endpoint,
            headers=self.headers,
            json={**parent.data, **icon.data, **cover.data,
                  "title": title_item.data, "properties": {**properties_data}})
        try:
            response.raise_for_status()
            out = response.json()
            self.db_id = out["id"]
            self.url = out["url"]
            self.title = db_title
            self.properties = list(out["properties"].keys())
            self.log(f"Created: {self}")
            return out
        except:
            print(response.text)


    def update(self,
            db_title: str = None,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = {}
        ) -> Dict:
        assert self.parent_id is not None, "You must specify a page/database parent id"
        properties = [p for p in properties if p.name not in self.properties]
        if len(properties)<1:
            self.log(f"Nothing to update in {self}")
            return
        icon = blocks.Icon(emoji=icon_emoji,url=icon_url)
        cover = blocks.Cover(url=cover_url)
        payload = {**icon.data, **cover.data}
        if db_title is not None:
            title_item = blocks.PageTitle(title=db_title)
            payload["title"] = title_item.data

        properties_data = {"Name": {"title": {}}}
        for p in properties:
            if isinstance(p, blocks.Rename):
                properties_data.update(p.data)
            else:
                properties_data.update(p.init_data)
        response = requests.patch(
            url=self.update_endpoint % self.db_id,
           headers=self.headers,
            json={**payload, "properties": {**properties_data}})
        try:
            response.raise_for_status()
            out = response.json()
            self.db_id = out["id"]
            self.url = out["url"]
            self.title = out["title"][0]["text"]["content"]
            self.log(f"Update: {self}")
            return out
        except:
            print(response.text)


    def add_page(self,
            page_title: str,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = []
         ) -> Tuple[Dict, page.Page]:
            p = page.Page(parent_id=self.db_id, logger=self.logger)
            out = p.create(
                add_in_db=True, page_title=page_title, icon_url=icon_url,
                icon_emoji=icon_emoji, cover_url=cover_url,
                properties=properties)
            return out, p

    def update_page(self,
            p: page.Page = None, page_id: str = None,
            page_title: str = None,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = []
         ) -> Tuple[Dict, page.Page]:
            assert p is None or page_id is None, "Specify page.Page object or page id"

            if p is None:
                p = page.Page(page_id=page_id, parent_id=self.db_id, logger=self.logger)

            out = p.update(page_title=page_title, icon_url=icon_url,
                     icon_emoji=icon_emoji, cover_url=cover_url,
                     properties=properties)
            return out, p

    def link_databases(self, p1: str, db2, p2: str, dual_prop: bool):
        if self.db_id is None or db2.db_id is None:
            self.log(f"{self} or {db2} is not created.")
            return
        if p1 in self.properties and p2 in db2.properties:
            self.log(f"Update: {p1} already exists in {self}. {p2} already exists in {db2}")
            return
        self.update(properties=[blocks.Relation(name=p1, related_db_id=db2.db_id, dual_prop=dual_prop)])
        if dual_prop:
            db2.update(properties=[blocks.Rename(name=f"Related to {self.title} ({p1})", new_name=p2)])


def create_db(root_page_id: str, params: Dict) -> Database:
    """Create Notion database from yml config file"""
    logger = logs.get_logger()
    db_icon = icons.IconUrl(name=params.get("icon"))
    db = Database(db_id=None, parent_id=root_page_id, logger=logger)
    properties = [
        getattr(blocks, item["block"])(**item.get("params", {}))
        for item in params.get("properties", [])
    ]
    db.create(db_title=params["name"], icon_url=db_icon.data, properties=properties)
    return db

def get_all_databases():
    logger = logs.get_logger()

