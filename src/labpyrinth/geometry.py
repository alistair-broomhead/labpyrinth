import typing

from pygame.math import Vector2


class Coordinate:
    down = (0, 1)
    up = (0, -1)
    right = (1, 0)
    left = (-1, 0)

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

    @property
    def as_tuple(self):
        return self.x, self.y

    @property
    def as_vector(self):
        return Vector2(self.x, self.y)

    def neighbours(self):
        yield self + self.up
        yield self + self.down
        yield self + self.left
        yield self + self.right


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

    def __repr__(self):
        return f'{type(self).__name__}{self.position,}'

    def __hash__(self):
        return hash((type(self), *self))

    def __iter__(self):
        yield from self.position.as_tuple

    @property
    def visited(self):
        return hasattr(self, 'connected_from') or self.is_start

    @property
    def assigned(self):
        return self.visited or self.is_end
