import os
import yaml
from typing import Dict
from datetime import datetime

def read_yml(fname: str) -> Dict:
    with open(fname, 'r') as f:
        return yaml.safe_load(f)

def time_to_seconds(t):
    for fmt in ("%H:%M:%S", "%M:%S"):
        try:
            parsed = datetime.strptime(t, fmt)
            return parsed.hour * 3600 + parsed.minute * 60 + parsed.second
        except ValueError:
            continue
    raise ValueError(f"Unrecognized time format: {t}")

def get_account_name(): return os.environ.get("NOTION_ACCOUNT_NAME")

def get_db_ids(account_name: str = None):
    if os.path.exists("db-ids.yml"):
        ids = read_yml("db-ids.yml")
        if ids is None:
            return {}
        if account_name is not None:
            return ids.get(account_name, {})
    return {}
