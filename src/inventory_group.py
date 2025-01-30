from typing import List
import yaml

from src import OUTPUT_DIR, is_prod

def update_inventory_group(environments: List[str], client_name: str):

    stage = "lower"
    if is_prod(environments):
        stage = "prod"
    
    for env in environments:
        file_path = f"./{OUTPUT_DIR}/{stage}/02-{env}.yml"
        with open(file_path, "r") as f:
            data = yaml.full_load(f)
            data[env]["children"][f"{client_name}_{env}"] = None

        with open(file_path, "w", encoding='utf-8') as f:
            yaml.dump(data, f, )

    