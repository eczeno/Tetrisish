#!/home/zeno/Desktop/tetris/.tetris/bin/python

import pytest
from tetris.tetris.tetris import Game

@pytest.fixture
def get_Game():
    
    return Game()

def test_init(get_Game):
    game = get_Game
    assert len(game.grid) == 20
    for row in game.grid:
        assert len(row) == 10