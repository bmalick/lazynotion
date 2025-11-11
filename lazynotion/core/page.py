import requests
from typing import Dict, List


from lazynotion.core import blocks
from lazynotion.core import auth
from lazynotion.core import display

class Page:
    endpoint = "https://api.notion.com/v1/pages"
    retrieve_endpoint = "https://api.notion.com/v1/pages/%s"
    retrieve_prop_endpoint = "https://api.notion.com/v1/pages/%s/properties/%s"
    update_endpoint = "https://api.notion.com/v1/pages/%s"

    def __init__(self, page_id: str = None, parent_id: str = None, logger = None):
        self.page_id = page_id
        self.parent_id = parent_id
        self.headers = auth.headers()
        self.logger = logger
        self.title = None
        self.url = None

    def __str__(self):
        return f"Database(title={self.title}, id={self.page_id}, parent={self.parent_id}, url={self.url})"

    def log(self, message: str):
        if self.logger is None:
            print(message)
        else:
            self.logger.info(message)

    def create(self,
            add_in_db: bool,
            page_title: str,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = []
        ) -> Dict:
        assert self.parent_id is not None, "You must specify a page/database parent id"
        parent = blocks.DatabaseParent(self.parent_id) if add_in_db else blocks.PageParent(self.parent_id)
        icon = blocks.Icon(emoji=icon_emoji,url=icon_url)
        cover = blocks.Cover(url=cover_url)
        title_item = blocks.PageTitle(title=page_title)
                    
        if not add_in_db :
            properties_data = {"title": title_item.data}
        else:
            properties_data = {
                "Name": {"title": [{"text": {"content": page_title}}]}
            }
        for p in properties:
            properties_data.update(p.data)

        response = requests.post(
            url=self.endpoint,
            headers=self.headers,
            json={
                **parent.data,
                **icon.data,
                **cover.data,
                "properties": {
                    **properties_data,
                }
                
            }
        )
        try:
            response.raise_for_status()
            out = response.json()
            self.page_id = out["id"]
            self.url = out["url"]
            self.page_id = out["id"]
            self.title = page_title
            self.log(f"[Page] Created: {self}")
            return out
        except:
            print(response.text)
    
    def retrieve(self) -> Dict:
        if self.page_id is None:
            self.log("[Page] Nothing to retrieve")
            return
        else:
            response = requests.get(
                url=self.retrieve_endpoint % self.page_id,
                headers=self.headers)
            try:
                response.raise_for_status()
                out = response.json()
                properties = ""
                for k,v in out["properties"].items():
                    k_val = v[v["type"]]
                    if isinstance(k_val, list) and len(k_val) > 0:
                        sub_type = k_val[0]["type"]
                        # k_val = k_val[0][sub_type]["content"]
                        k_val = k_val[0][sub_type]
                    elif isinstance(k_val, dict) and len(k_val) > 0:
                        if "type" in k_val:
                            sub_type = k_val["type"]
                            k_val = k_val[sub_type]
                    properties += f"    {k}: {k_val}\n".ljust(-4)

                self.log(display.PAGE_RETRIEVE.format(**out, props=properties))
                return out
            except:
                print(response.text)

    def update(self,
            page_title: str = None,
            icon_url: str = None,
            icon_emoji: str = None,
            cover_url: str = None,
            properties: List[blocks.DataProperty] = []
        ) -> Dict:
        assert self.parent_id is not None, "You must specify a page/database parent id"
        icon = blocks.Icon(emoji=icon_emoji,url=icon_url)
        cover = blocks.Cover(url=cover_url)
        payload = {**icon.data, **cover.data}

        if page_title is not None:
            properties_data = {
                "Name": {"type": "title", "title": [{"text": {"content": page_title}}]}
            }
        else: properties_data = {}
        for p in properties:
            properties_data.update(p.data)

        response = requests.patch(
            url=self.update_endpoint % self.page_id,
            headers=self.headers,
            json={**payload, "properties": {**properties_data}})
        try:
            response.raise_for_status()
            out = response.json()
            self.page_id = out["id"]
            self.url = out["url"]
            self.title = page_title
            self.log(f"[Page]: {self}")
            return out
        except:
            print(response.text)

    def delete(self) -> None:
        # TODO
        pass
