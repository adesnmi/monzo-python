import json
from monzo.const import MONZO_CACHE_FILE

def save_token_to_file(token, filename=MONZO_CACHE_FILE):
    """Saves a token dictionary to a json file"""
    with open(filename, 'w') as fp:
        json.dump(token, fp, sort_keys=True, indent=4)

def load_token_from_file(filename=MONZO_CACHE_FILE):
    """Loads a json file and returns a dictionary of its contents"""
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return data
