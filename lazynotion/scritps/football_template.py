from typing import Dict

import lazynotion

def create_db(params: Dict) -> lazynotion.database.Database:
    """Create Notion database from yml config file"""
    global logger, root_page_id
    db_icon = lazynotion.icons.IconUrl(name=params["icon"])
    db_cover = params.get("cover")
    db = lazynotion.database.Database(db_id=None, parent_id=root_page_id, logger=logger)
    properties = [
        getattr(lazynotion.blocks, item["block"])(**item.get("params", {}))
        for item in params["properties"]
    ]
    db.create(db_title=params["name"], icon_url=db_icon.data, properties=properties)
    return db

if __name__ == "__main__":
    logger = lazynotion.logs.get_logger()
    football_cfg = lazynotion.utils.read_yml("lazynotion/configs/football-template.yml")
    root_page_id = football_cfg["root_page"]
    all_dbs = {}

    for db_params in football_cfg["databases"]:
        db_name = db_params["name"].lower().replace(' ','_')
        all_dbs[db_name] = create_db(db_params)

    # Databases relations linking
    if "relations" in football_cfg:
        for params in football_cfg["relations"]:
            db1 = all_dbs[params["db1"]]
            db2 = all_dbs[params["db2"]]
            p1 = params["p1"]
            p2 = params["p2"]
            db1.link_databases(p1=p1, db2=db2, p2=p2)


    # for db_params in football_cfg["databases"]:
    #     db_name = db_params["name"].lower().replace(' ','_')
    #     if "update_properties" in db_params:
    #         all_dbs[db_name].update(properties=[
    #             getattr(lazynotion.blocks, item["block"])(**item.get("params", {}))
    #             for item in db_params["update_properties"]
    #         ])
























