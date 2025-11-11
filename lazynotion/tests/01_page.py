import yaml

import lazynotion

if __name__ == "__main__":

    with open("keys.yml", "r") as f:
        cfg = yaml.safe_load(f)

    logger = lazynotion.logs.get_logger()
    # page = lazynotion.page.Page(page_id=None, parent_id=cfg["test_page"], logger=logger)
    # out = page.create(add_in_db=False, page_title="test page creation", icon_emoji="🥬", cover_url="https://images.pexels.com/photos/10793922/pexels-photo-10793922.jpeg")
    # created_page_id = out["id"]
    created_page_id = "2a8205400a928012a451c6f2484aab99"
    page = lazynotion.page.Page(page_id=created_page_id, logger=logger)
    out = page.retrieve()
    print(out)


