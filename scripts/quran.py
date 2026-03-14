import yaml
from datetime import datetime

from src import lazynotion

if __name__=="__main__":
    saved_ids = lazynotion.utils.get_db_ids(lazynotion.utils.get_account_name())
    surahs = lazynotion.utils.read_yml("configs/quran.yml")["surahs"]
    surah_icon = lazynotion.icons.IconUrl(name="book_open")

    db_id = saved_ids["quran"]
    db = lazynotion.database.Database(db_id=db_id)
    for surah in surahs:
        db.add_page(
            page_title=surah["name"],
            icon_url=surah_icon.data,
            properties=[lazynotion.blocks.Number(name="Number", number=surah["number"]),
                        lazynotion.blocks.Number(name="Total ayahs", number=surah["total_ayahs"]),
                        lazynotion.blocks.Text(name="Time recitation", text=surah["time"]),
                        lazynotion.blocks.Number(name="Time recitation in seconds", number=lazynotion.utils.time_to_seconds(surah["time"])),
                        lazynotion.blocks.Url(name="Surah info", url=surah["info"]),
                        lazynotion.blocks.Url(name="Url", url=surah["url"]), 
                        ])

