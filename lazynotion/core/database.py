import requests
from typing import Dict, List, Tuple


from lazynotion.core import blocks
from lazynotion.core import auth
from lazynotion.core import page
from lazynotion.core import display

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

    def create(self,
            db_title: str,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = {}
        ) -> Dict:
        assert self.parent_id is not None, "You must specify a page/database parent id"
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
            new_id = out["id"]
            new_url = out["url"]
            if self.logger is not None:
                self.logger.info(f"[Created database]: title={db_title}, id={new_id}, parent={self.parent_id}, url={new_url}")

            self.db_id = new_id
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
        icon = blocks.Icon(emoji=icon_emoji,url=icon_url)
        cover = blocks.Cover(url=cover_url)
        payload = {**icon.data, **cover.data}
        if db_title is not None:
            title_item = blocks.PageTitle(title=db_title)
            payload["title"] = title_item.data


        properties_data = {"Name": {"title": {}}}
        for p in properties:
            properties_data.update(p.data)
        response = requests.patch(
            url=self.update_endpoint % self.db_id,
            headers=self.headers,
            json={**payload, "properties": {**properties_data}})
        try:
            response.raise_for_status()
            out = response.json()
            new_id = out["id"]
            new_url = out["url"]
            if self.logger is not None:
                self.logger.info(f"[Updated database]: title={db_title}, id={new_id}, parent={self.parent_id}, url={new_url}")

            self.db_id = new_id
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

    # def add_page(self,
    #         page_title: str,
    #         icon_url: str = None,
    #         icon_emoji: str = None,
    #         cover_url: str = None,
    #         properties: List[blocks.DataProperty] = []
    #      ) -> Tuple[Dict, page.Page]:
    #         p = page.Page(parent_id=self.db_id, logger=self.logger)
    #         out = p.create(
    #             add_in_db=True, page_title=page_title, icon_url=icon_url,
    #             icon_emoji=icon_emoji, cover_url=cover_url,
    #             properties=properties)
    #         return out, p
