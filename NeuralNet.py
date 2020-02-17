#!/usr/bin/env python3

from sklearn import neural_network
import random
import sys

import Autoplay
import Board


def learn(epochs, verbose=False):
    model = neural_network.MLPClassifier()
    board = Board.Board(4, 4)
    classes = ["u", "d", "l", "r"]
    model.partial_fit(
        [board.get_game_state()],
        ["u"],
        classes=classes
    )
    for epoch in range(epochs):
        board = Board.Board(4, 4)
        movement = {
            "u": board.up,
            "d": board.down,
            "l": board.left,
            "r": board.right
        }
        score = board.get_score()
        while not board.game_over():
            prev_state = board.get_game_state()
            prediction = model.predict([prev_state])[0]
            while not movement[prediction]():
                prediction = random.choice(classes)
            if board.get_score() > score:
                model.partial_fit([prev_state], [prediction])
                score = board.get_score()
            board.spawn_tile()
        sys.stdout.write("\033[K")
        if verbose:
            print(f"Epoch {epoch + 1}, score: {board.get_score()}", end="\r")
    if verbose:
        print()
    return model


if __name__ == "__main__":
    print("Learning to play 2048...")
    MODEL = learn(10_000, verbose=True)
    Autoplay.model_play(MODEL)
