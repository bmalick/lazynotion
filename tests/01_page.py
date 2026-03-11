import os

from src import lazynotion

if __name__ == "__main__":
    logger = lazynotion.logs.get_logger()
    page = lazynotion.page.Page(page_id=None, parent_id=os.environ["DATABASES_PAGE"], logger=logger)
    out = page.create(add_in_db=False, page_title="test page creation", icon_emoji="🥬", cover_url="https://images.pexels.com/photos/10793922/pexels-photo-10793922.jpeg")
    created_page_id = out["id"]
    page = lazynotion.page.Page(page_id=created_page_id, logger=logger)
    out = page.retrieve()
    print(out)
