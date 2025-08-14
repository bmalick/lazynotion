import yaml

import lazynotion

if __name__ == "__main__":

    with open("keys.yml", "r") as f:
        cfg = yaml.safe_load(f)

    parent_id = cfg["test_page"]
    logger = lazynotion.logs.get_logger()

    book_db = lazynotion.database.Database(db_id=None, parent_id=parent_id, logger=logger)
    properties1 = [
        lazynotion.blocks.PropertyText("Title"),
        lazynotion.blocks.PropertyNumber("Number of pages"),
        lazynotion.blocks.PropertySelect("Genre", options=[
            ("Fiction", "green"),
            ("Sci-Fi", "blue"),
            ("Novel", "red")
        ]),
        lazynotion.blocks.PropertyDate("Start"),
        # lazynotion.blocks.PropertySelect("Empty select", options=[]),
        # lazynotion.blocks.PropertyMultiSelect("Empty multi select", options=[]),
        # lazynotion.blocks.PropertyMultiSelect("Studies", options=[
        #     ("Maths", "green"),
        #     ("Physics", "red")
        # ]),
    ]
    icon_book = lazynotion.icons.IconUrl(name="book-closed")
    out1 = book_db.create(db_title="Books", properties=properties1, icon_url=icon_book.data)

    author_db = lazynotion.database.Database(db_id=None, parent_id=parent_id, logger=logger)
    properties2 = [
        lazynotion.blocks.PropertyDate(name="Birth Year"),
        # lazynotion.blocks.PropertyPeople("People"),
        # # lazynotion.blocks.PropertyFile("File"),
        # lazynotion.blocks.PropertyCheckbox("Checkbox"),
        # lazynotion.blocks.PropertyUrl("Url"),
        # lazynotion.blocks.PropertyEmail("Email"),
        # lazynotion.blocks.PropertyFormula("Formula"),
        lazynotion.blocks.PropertyRelation(name="Books", related_db_id=out1["id"]),
        lazynotion.blocks.PropertyRollup(name="Number of publications", rollup_property_name="Name", relation_property_name="Books", function="count"),
        # lazynotion.blocks.PropertyPhonenumber("Phonenumber"),
        # lazynotion.blocks.PropertyCreatedtime("Createdtime"),
        # lazynotion.blocks.PropertyLastEditedtime("LastEditedtime"),
    ]
    icon_author = lazynotion.icons.IconUrl(name="user")
    out2 = author_db.create(db_title="Authors", properties=properties2, icon_url=icon_author.data)

    book_db.update(properties=[lazynotion.blocks.RenameProperty(current_name="Related to Authors (Books)", new_name="Author")])


    out3, p = author_db.add_page(
        page_title="Mariama Bâ",
        icon_url=icon_author.data)

    properties1[3].update(start="2025-08-14")
    properties1[1].update(number=171)
    book1_props = [
        properties1[1],
        properties1[3],
        lazynotion.blocks.PropertyRelation(name="Author", related_db_id=out1["id"], relation_ids=[out3["id"]])
    ]
    out4, book1 = book_db.add_page(
        page_title="Une si longue lettre",
        icon_url=icon_book.data,
        properties=book1_props
    )

    properties1[2].update(option="Novel")
    book1.update(properties=[properties1[2]])

