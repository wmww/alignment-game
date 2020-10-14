import pytest # type: ignore
from state import read_state, remove_state_file
from game import Game

TEST_STATE_FILEPATH = 'test_state.json'

class TestGame():
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield

        remove_state_file(TEST_STATE_FILEPATH)

    def test_state_bootstrap(self):
        state = read_state(TEST_STATE_FILEPATH)

        GRID_SIZE = 3
        game = Game(state, bootstrap_grid_size=GRID_SIZE, write_state = lambda x: None)

        for i in range(GRID_SIZE):
            assert len(game.state['grid'][i]) == GRID_SIZE
        
        USER_ID = 0
        game.register_player({
            'user_id': USER_ID,
            'username': 'testuser',
            'pfp_path': '',
        }, spawn_x=1, spawn_y=2)
        
        player_square = game.get_square(1, 2)

        assert player_square['player'] == USER_ID

        
