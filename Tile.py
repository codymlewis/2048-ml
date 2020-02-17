'''
Object for the 2048 tile
'''


class Tile:
    '''
    2048 Tile class
    '''

    def __init__(self, value, max_num_len=1):
        self.__value = value
        self.max_num_len = max(max_num_len, len(str(value)))

    def __add__(self, other):
        return Tile(self.__value + int(other))

    def __eq__(self, other):
        return isinstance(other, Tile) and self.__value == int(other)

    def __str__(self):
        return f"{self.__value:{self.max_num_len}d}"

    def __int__(self):
        return self.__value
