import os
import yaml
from argparse import ArgumentParser

from src import lazynotion

def main():
    parser = ArgumentParser()
    parser.add_argument("--config", "-c", required=True, type=str)
    args = parser.parse_args()

    data_cfg = lazynotion.utils.read_yml(args.config)
    root_page_id = os.environ[data_cfg["root_page"]]
    notion_account_name = lazynotion.utils.get_account_name()

    if notion_account_name is None:
        print("No notion account specified. Please fill NOTION_ACCOUNT_NAME in keys.sh")
        return None

    all_dbs = {}
    db_ids = {notion_account_name: {}}
    
    for db_params in data_cfg["databases"]:
        db_name = db_params["name"].lower().replace(' ','-')
        all_dbs[db_name] = lazynotion.database.create_db(root_page_id, db_params)
        db_ids[notion_account_name][db_name] = all_dbs[db_name].db_id

    # Databases relations linking
    for params in data_cfg.get("relations", []):
        db1 = all_dbs.get(params["db1"])
        db2 = all_dbs.get(params["db2"])
        p1 = params["p1"]
        p2 = params["p2"]
        db1.link_databases(p1=p1, db2=db2, p2=p2, dual_prop=params.get("dual_prop", False))

    # Databases rollup
    for item in data_cfg.get("rollups", []):
        properties = [getattr(lazynotion.blocks, p["block"])(**p.get("params", {}))
            for p in item.get("properties", [])]
        all_dbs[item["name"]].update(properties=properties)


    for db_params in data_cfg["databases"]:
        db_name = db_params["name"].lower().replace(' ','-')
        if "update_properties" in db_params:
            all_dbs[db_name].update(properties=[
                getattr(lazynotion.blocks, item["block"])(**item.get("params", {}))
                for item in db_params["update_properties"]
            ])
    saved_ids = lazynotion.utils.get_db_ids()
    saved_ids.update(db_ids)
    with open("db-ids.yml", "w") as f:
        yaml.safe_dump(saved_ids, f)


if __name__ == "__main__": main()
