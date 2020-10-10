from typing import Callable, TypedDict, List
from random import randint

from state import read_state, write_state

class Player(TypedDict):
    user_id: str
    username: str
    pfp_path: str

class Square(TypedDict):
    claimant: str # Should be a user_id
    territory: str # Unsure how to model atm
    player: str # user_id, represents the player currently in the location

class GameState(TypedDict):
    grid: List[List[Square]]
    players: List[Player]

class Game():
    def __init__(
        self,
        state: GameState,
        # Called "bootstrap" as we only use this when we don't have a grid--
        # runtime size is pulled from the actual internal state
        bootstrap_grid_size: int = 100,
        write_state: Callable[[GameState, str], None] = write_state
    ):
        self.state = state
        self._write_state = write_state

        if 'grid' not in self.state:
            self.build_grid(bootstrap_grid_size)
        
        self.grid_size = len(self.state['grid'])
    
    def write_state(self):
        self._write_state(self.state)
    
    def build_grid(self, size: int):
        self.state['grid'] = []

        for i in range(size):
            row = []

            for j in range(size):
                row.append({
                    'claimant': None,
                    'territory': None,
                    'player': None,
                })

            self.state['grid'].append(row)
        self.write_state()
    
    def _random_square(self):
        x = randint(0, self.grid_size - 1)
        y = randint(0, self.grid_size - 1)
        return self.state['grid'][x][y]
    
    def get_square(self, spawn_x: int, spawn_y: int):
        return self.state['grid'][spawn_x][spawn_y]
    
    def register_player(self, player: Player, spawn_x: int, spawn_y: int):
        self.state['players'].append(player)

        if spawn_x and spawn_y:
            square = self.get_square(spawn_x, spawn_y)
        else:
            square = self._random_square()

        square['player'] = player['user_id']

        self.write_state()


