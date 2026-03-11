import os

from src import lazynotion

if __name__ == "__main__":
    parent_id = os.environ["DATABASES_PAGE"]
    logger = lazynotion.logs.get_logger()

    book_db = lazynotion.database.Database(db_id=None, parent_id=parent_id, logger=logger)
    properties1 = [
        lazynotion.blocks.Text("Title"),
        lazynotion.blocks.Number("Number of pages"),
        lazynotion.blocks.Select("Genre", init_options=[
            ("Fiction", "green"),
            ("Sci-Fi", "blue"),
            ("Novel", "red")
        ]),
        lazynotion.blocks.Date("Start"),
        # lazynotion.blocks.Select("Empty select", options=[]),
        # lazynotion.blocks.MultiSelect("Empty multi select", options=[]),
        # lazynotion.blocks.MultiSelect("Studies", options=[
        #     ("Maths", "green"),
        #     ("Physics", "red")
        # ]),
    ]
    icon_book = lazynotion.icons.IconUrl(name="book-closed")
    out1 = book_db.create(db_title="TestBooks", properties=properties1, icon_url=icon_book.data)

    author_db = lazynotion.database.Database(db_id=None, parent_id=parent_id, logger=logger)
    properties2 = [
        lazynotion.blocks.Date(name="Birth Year"),
        # lazynotion.blocks.People("People"),
        # # lazynotion.blocks.File("File"),
        # lazynotion.blocks.Checkbox("Checkbox"),
        # lazynotion.blocks.Url("Url"),
        # lazynotion.blocks.Email("Email"),
        # lazynotion.blocks.Formula("Formula"),
        lazynotion.blocks.Relation(name="Books", related_db_id=out1["id"], dual_prop=True),
        lazynotion.blocks.Rollup(name="Number of publications", rollup_property_name="Name", relation_property_name="Books", function="count"),
        # lazynotion.blocks.Phonenumber("Phonenumber"),
        # lazynotion.blocks.Createdtime("Createdtime"),
        # lazynotion.blocks.LastEditedtime("LastEditedtime"),
    ]
    icon_author = lazynotion.icons.IconUrl(name="user")
    out2 = author_db.create(db_title="TestAuthors", properties=properties2, icon_url=icon_author.data)



    out3, p = author_db.add_page(
        page_title="Mariama Bâ",
        icon_url=icon_author.data)

    properties1[3].update(start="2025-08-14")
    properties1[1].update(number=171)
    book1_props = [
        properties1[1],
        properties1[3],
        lazynotion.blocks.Relation(name="Author", related_db_id=out1["id"], relation_ids=[out3["id"]])
    ]
    out4, book1 = book_db.add_page(
        page_title="Une si longue lettre",
        icon_url=icon_book.data,
        properties=book1_props
    )

    properties1[2].update(options="Novel")
    # book1.update(properties=[properties1[2]])
    book_db.update_page(p=book1, properties=[properties1[2]])

