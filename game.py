#!/usr/bin/env python3

from getkey import getkey, keys

import Board

if __name__ == "__main__":
    board = Board.Board(4, 4)
    movement = {
        keys.UP: board.up,
        keys.DOWN: board.down,
        keys.LEFT: board.left,
        keys.RIGHT: board.right
    }
    print(board)
    while not board.game_over():
        print("Your move: ")
        key = getkey()
        moved = False
        if key in movement.keys():
            moved = movement[key]()
        if moved:
            board.spawn_tile()
            print()
            print(board)
    print("Game over!")
    print(f"Final score: {board.get_score()}")
