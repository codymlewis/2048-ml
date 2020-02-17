import itertools
import numpy as np

import Board


'''
Functions that play 2048 without user input
'''


def convert_and_play(moves):
    '''Convert the list of moves and play the game with it'''
    return np.mean([play(str().join(moves)) for _ in range(10)])


def play(move_str, verbose=False):
    '''Play the game by cycling the moves specified'''
    board = Board.Board(4, 4)
    movement = {
        "u": board.up,
        "d": board.down,
        "l": board.left,
        "r": board.right
    }
    counter = 0
    if verbose:
        print(board)
    for a in itertools.cycle(move_str):
        if board.game_over() or counter == len(move_str):
            break
        if movement[a]():
            board.spawn_tile()
            counter = 0
            if verbose:
                print()
                print(board)
        else:
            counter += 1
    return board.get_score()


def model_play(model):
    board = Board.Board(4, 4)
    movement = {
        "u": board.up,
        "d": board.down,
        "l": board.left,
        "r": board.right
    }
    print(board)
    while not board.game_over()and \
            movement[model.predict([board.get_game_state()])[0]]():
        board.spawn_tile()
        print(board)
    print("Game over!")
    print(f"The model scored {board.get_score()}!")
