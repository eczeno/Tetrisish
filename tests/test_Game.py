#!/home/zeno/Desktop/tetris/.tetris/bin/python

import pytest
from tetris.tetris.tetris import Game

@pytest.fixture
def game():
    return Game()

def test_init(game):
    assert len(game.grid) == 20
    for row in game.grid:
        assert len(row) == 10


def test_is_valid_space(game):
    assert game.is_valid_space() == True
