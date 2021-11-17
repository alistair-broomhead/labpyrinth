import typing

from pygame.math import Vector2

start_symbol = '😀'
end_symbol = '🏁'


class Coordinate:
    moves: 'typing.Dict[Coordinate, str]'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        x, y = other
        return x == self.x and y == self.y

    def __repr__(self):
        return f'{type(self).__name__}{self.as_tuple}'

    def __iter__(self):
        yield from self.as_tuple

    @property
    def as_tuple(self):
        return self.x, self.y

    @property
    def as_vector(self):
        return Vector2(self.x, self.y)

    def __add__(self, other):
        x, y = other

        return type(self)(self.x + x, self.y + y)

    def __sub__(self, other):
        x, y = other

        return type(self)(self.x - x, self.y - y)

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __mul__(self, scale: int):
        return type(self)(self.x * scale, self.y * scale)

    def __hash__(self):
        return hash((type(self), *self))

    def neighbours(self):
        for move in self.moves.keys():
            yield self + move


# Now that we have a class we can store these objects on it
Coordinate.moves = {
    Coordinate(0, 1): '↓',
    Coordinate(1, 0): '→',
    Coordinate(0, -1): '↑',
    Coordinate(-1, 0): '←',
}


class Square:
    connected_from: Coordinate
    connected_to: typing.List[Coordinate]

    is_start = False
    is_end = False

    def __init__(self, position: Coordinate):
        self.position = position
        self.connected_to = []

    def from_(self, other: 'Square'):
        vector = self.position - other.position
        self.connected_from = vector
        other.connected_to.append(vector)
        return self

    @property
    def symbols(self):
        if self.is_start:
            yield start_symbol
        if self.is_end:
            yield end_symbol

        for x in self.connected_to:
            yield Coordinate.moves[x]

        if (not self.connected_to) and self.visited and (not self.is_end):
            yield 'x'

    def __repr__(self):
        return f'{type(self).__name__}{*self.position, *self.symbols}'

    def __hash__(self):
        return hash((type(self), *self))

    def __iter__(self):
        yield from self.position.as_tuple

    @property
    def visited(self):
        return hasattr(self, 'connected_from') or self.is_start
