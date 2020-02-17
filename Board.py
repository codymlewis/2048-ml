import math
import random

import Tile


'''
Object for the 2048 Board
'''


class Board:
    '''
    A 2048 board class
    '''

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__score = 0
        self.__tiles = [[None for _ in range(width)] for _ in range(height)]
        self.__max_num_len = 1
        self.__available_tiles = [i for i in range(width * height)]
        for _ in range(1 if random.randint(1, 100) < 95 else 2):
            self.spawn_tile()

    def get_game_state(self):
        '''Return a flattened list of the current game state'''
        return [int(t) if t else 0 for r in self.__tiles for t in r]

    def get_score(self):
        '''Get the current score of the game'''
        return self.__score

    def spawn_tile(self):
        '''Spawn a random new Tile on the board'''
        coord = random.sample(self.__available_tiles, 1)[0]
        i = coord % self.__width
        j = math.floor(coord / self.__width)
        self.__tiles[i][j] = Tile.Tile(
            2 if random.randint(1, 100) < 95 else 4,
            self.__max_num_len
        )
        self.take_space(i, j)

    def take_space(self, col, row):
        '''Mark a space in the board as taken'''
        self.__available_tiles.remove(row * self.__width + col)

    def give_space(self, col, row):
        '''Unmark a space in the board as taken'''
        self.__available_tiles.append(row * self.__width + col)

    def combine_tiles(self, i, j, k, l):
        '''Combine 2 tiles on the board'''
        self.__tiles[k][l] += self.__tiles[i][j]
        self.__tiles[i][j] = None
        self.give_space(i, j)
        self.__score += int(self.__tiles[k][l])
        if self.__tiles[k][l].max_num_len > self.__max_num_len:
            self.update_mnl(self.__tiles[k][l].max_num_len)
        else:
            self.__tiles[k][l].max_num_len = self.__max_num_len

    def update_mnl(self, new_len):
        '''Update the maximum number length'''
        self.__max_num_len = new_len
        for i in range(self.__height):
            for j in range(self.__width):
                if self.__tiles[i][j]:
                    self.__tiles[i][j].max_num_len = new_len

    def move_tile(self, i, j, k, l):
        '''Move a tile across the board'''
        if i != k or j != l:
            self.__tiles[k][l] = self.__tiles[i][j]
            self.take_space(k, l)
            self.__tiles[i][j] = None
            self.give_space(i, j)

    def game_over(self):
        '''Check when the game is over'''
        return len(self.__available_tiles) == 0 and self.no_adjacents()

    def no_adjacents(self):
        '''Check that there are no equal adjecent tiles'''
        for i in range(self.__height):
            for j in range(self.__width):
                p = j < self.__width - 1 and self.__tiles[i][j + 1] == self.__tiles[i][j]
                q = i < self.__height - 1 and self.__tiles[i + 1][j] == self.__tiles[i][j]
                if p or q:
                    return False
        return True

    def left(self):
        '''Slide the tiles to the left'''
        if not self.can_left():
            return False
        for i in range(self.__height):
            pivot = 0
            for j in range(1, self.__width):
                if self.__tiles[i][j]:
                    if self.__tiles[i][j] == self.__tiles[i][pivot]:
                        self.combine_tiles(i, j, i, pivot)
                    else:
                        if self.__tiles[i][pivot]:
                            pivot += 1
                        self.move_tile(i, j, i, pivot)
        return True

    def can_left(self):
        '''Check if anything can move left'''
        for i in range(self.__height):
            for j in range(1, self.__width):
                p = self.__tiles[i][j]
                q = not self.__tiles[i][j - 1] or \
                    self.__tiles[i][j] == self.__tiles[i][j - 1]
                if p and q:
                    return True
        return False

    def right(self):
        '''Slide the tiles to the right'''
        if not self.can_right():
            return False
        for i in range(self.__height - 1, -1, -1):
            pivot = self.__width - 1
            for j in range(self.__width - 2, -1, -1):
                if self.__tiles[i][j]:
                    if self.__tiles[i][j] == self.__tiles[i][pivot]:
                        self.combine_tiles(i, j, i, pivot)
                    else:
                        if self.__tiles[i][pivot]:
                            pivot -= 1
                        self.move_tile(i, j, i, pivot)
        return True

    def can_right(self):
        '''Check if anything can move right'''
        for i in range(self.__height - 1, -1, -1):
            for j in range(self.__width - 2, -1, -1):
                p = self.__tiles[i][j]
                q = not self.__tiles[i][j + 1] or \
                    self.__tiles[i][j] == self.__tiles[i][j + 1]
                if p and q:
                    return True
        return False

    def up(self):
        '''Slide the tiles up'''
        if not self.can_up():
            return False
        for j in range(self.__width):
            pivot = 0
            for i in range(1, self.__height):
                if self.__tiles[i][j]:
                    if self.__tiles[i][j] == self.__tiles[pivot][j]:
                        self.combine_tiles(i, j, pivot, j)
                    else:
                        if self.__tiles[pivot][j]:
                            pivot += 1
                        self.move_tile(i, j, pivot, j)
        return True

    def can_up(self):
        '''Check if anything can move up'''
        for j in range(self.__width):
            for i in range(1, self.__height):
                p = self.__tiles[i][j]
                q = not self.__tiles[i - 1][j] or \
                    self.__tiles[i][j] == self.__tiles[i - 1][j]
                if p and q:
                    return True
        return False

    def down(self):
        '''Slide the tiles down'''
        if not self.can_down():
            return False
        for j in range(self.__width - 1, -1, -1):
            pivot = self.__width - 1
            for i in range(self.__height - 2, -1, -1):
                if self.__tiles[i][j]:
                    if self.__tiles[i][j] == self.__tiles[pivot][j]:
                        self.combine_tiles(i, j, pivot, j)
                    else:
                        if self.__tiles[pivot][j]:
                            pivot -= 1
                        self.move_tile(i, j, pivot, j)
        return True

    def can_down(self):
        '''Check if anything can move down'''
        for j in range(self.__width - 1, -1, -1):
            for i in range(self.__height - 2, -1, -1):
                p = self.__tiles[i][j]
                q = not self.__tiles[i + 1][j] or \
                    self.__tiles[i][j] == self.__tiles[i + 1][j]
                if p and q:
                    return True
        return False

    def __str__(self):
        result = f"Score: {self.__score}\n"
        for i in range(self.__height):
            result += ("_" if i == 0 else "=") * \
                (self.__width * (self.__max_num_len + 2)) + "\n"
            for j in range(self.__width):
                result += "|" + \
                    (str(self.__tiles[i][j]) if self.__tiles[i][j]
                        else " " * self.__max_num_len) + "|"
            result += "\n"
        result += "-" * (self.__width * (self.__max_num_len + 2)) + "\n"
        return result
