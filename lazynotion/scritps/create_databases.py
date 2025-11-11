import os
import sys
import yaml
from typing import Dict

import lazynotion


if __name__ == "__main__":
    data_cfg = lazynotion.utils.read_yml(sys.argv[1])
    root_page_id = os.environ[data_cfg["root_page"]]
    all_dbs = {}
    db_ids = {}
    
    for db_params in data_cfg["databases"]:
        db_name = db_params["name"].lower().replace(' ','_')
        all_dbs[db_name] = lazynotion.database.create_db(root_page_id, db_params)
        db_ids[db_name] = all_dbs[db_name].db_id

    # Databases relations linking
    if "relations" in data_cfg:
        for params in data_cfg["relations"]:
            db1 = all_dbs[params["db1"]]
            db2 = all_dbs[params["db2"]]
            p1 = params["p1"]
            p2 = params["p2"]
            db1.link_databases(p1=p1, db2=db2, p2=p2)


    for db_params in data_cfg["databases"]:
        db_name = db_params["name"].lower().replace(' ','_')
        if "update_properties" in db_params:
            all_dbs[db_name].update(properties=[
                getattr(lazynotion.blocks, item["block"])(**item.get("params", {}))
                for item in db_params["update_properties"]
            ])
    try:
        with open("db-ids.yml", "r") as f:
            saved_ids = yaml.safe_load(f)
    except FileNotFoundError:
        saved_ids = {}
    saved_ids.update(db_ids)
    with open("db-ids.yml", "w") as f:
        yaml.safe_dump(saved_ids, f)


