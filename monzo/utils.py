import json
from monzo.const import MONZO_CACHE_FILE

def save_token_to_file(token, filename=MONZO_CACHE_FILE):
    with open(filename, 'w') as fp:
        json.dump(token, fp, sort_keys=True, indent=4)

def load_token_from_file(filename=MONZO_CACHE_FILE):
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data
