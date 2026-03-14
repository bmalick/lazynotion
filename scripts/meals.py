from typing import Dict

from src import lazynotion

if __name__=="__main__":
    saved_ids = lazynotion.utils.get_db_ids(lazynotion.utils.get_account_name())
    meals = lazynotion.utils.read_yml("configs/meals.yml")["meals"]
    meal_icon = lazynotion.icons.IconUrl(name="dining")

    db_id = saved_ids["meals"]
    db = lazynotion.database.Database(db_id=db_id)
    for meal in meals:
        db.add_page(
            page_title=meal["name"],
            icon_url=meal_icon.data,
            properties=[lazynotion.blocks.Url(name="Url", url=meal["url"]),
                        lazynotion.blocks.Select(name="Type", options=meal["type"])]
        )

