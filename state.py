import json
import os

INIT_STATE = {
    'players': [],
    # grid here, absence used to indicate to Game to instantiate it
}
JSON_FILEPATH = 'state.json'

def init_state_file(filepath: str = JSON_FILEPATH) -> None:
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(json.dumps(INIT_STATE))

def remove_state_file(filepath: str) -> None:
    os.remove(filepath)

def write_state(dict: dict, filepath: str = JSON_FILEPATH) -> None:
    with open(filepath, 'w') as f:
        json.dump(f)

def read_state(filepath: str = JSON_FILEPATH) -> dict:
    init_state_file(filepath)

    with open(filepath, 'r') as f:
        return json.load(f)
