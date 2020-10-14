import json
import os
from typing import cast, TypedDict, List, Optional

class Player(TypedDict):
    user_id: str
    username: str
    pfp_path: str

class Square(TypedDict):
    claimant: Optional[str] # Should be a user_id
    territory: Optional[str] # Unsure how to model atm
    player: Optional[str] # user_id, represents the player currently in the location

class GameState(TypedDict):
    grid: List[List[Square]]
    players: List[Player]

INIT_STATE: GameState = {
    'players': [],
    'grid': [],
}
JSON_FILEPATH = 'state.json'

def init_state_file(filepath: str = JSON_FILEPATH) -> None:
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(json.dumps(INIT_STATE))

def remove_state_file(filepath: str) -> None:
    os.remove(filepath)

def write_state(state: GameState, filepath: str = JSON_FILEPATH) -> None:
    with open(filepath, 'w') as f:
        json.dump(state, f)

def read_state(filepath: str = JSON_FILEPATH) -> GameState:
    init_state_file(filepath)

    with open(filepath, 'r') as f:
        return cast(GameState, json.load(f))
