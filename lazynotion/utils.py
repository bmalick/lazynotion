import yaml
from typing import Dict

def read_yml(fname: str) -> Dict:
    with open(fname, 'r') as f:
        return yaml.safe_load(f)
