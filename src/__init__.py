from typing import List

OUTPUT_DIR = "inventory"

def is_prod(env: List[str]) -> bool:
    return "prod" in env