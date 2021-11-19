import itertools
import typing

from pygame.math import Vector2


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        x, y = other
        return x == self.x and y == self.y

    def __repr__(self):
        return f'{type(self).__name__}{*self,}'

    def __iter__(self):
        yield from [self.x, self.y]

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
    def as_vector(self):
        return Vector2(self.x, self.y)


class Direction:
    up = Coordinate(0, -1)
    down = Coordinate(0, 1)
    left = Coordinate(-1, 0)
    right = Coordinate(1, 0)

    all = frozenset((up, down, left, right))

    _int_lookup = {
        # Used for a bitfield of sides
        up: 1,
        down: 2,
        left: 4,
        right: 8,
    }

    @classmethod
    def to_int(cls, *directions: Coordinate):
        return sum(
            cls._int_lookup.get(direction, 0) for direction in directions
        )

    @classmethod
    def combinations(cls) -> typing.Iterable[typing.Tuple['Direction']]:
        yield ()

        for direction in cls.all:
            yield direction,

        for length in range(1, len(cls.all)):
            length += 1

            for selected in itertools.permutations(cls.all, length):
                yield selected


class Square:
    connected_from: Coordinate
    connected_to: typing.Set[Coordinate]

    is_start = False
    is_end = False

    def __init__(self, position: Coordinate):
        self.position = position
        self.connected_to = set()

    def open_sides(self):
        if from_ := getattr(self, 'connected_from', False):
            yield from_
        yield from self.connected_to

    def closed_sides(self):
        sides = Direction.all - set(self.open_sides())
        yield from sides

    def neighbour_positions(self) -> typing.Iterable[Coordinate]:
        for direction in Direction.all:
            yield self.position + direction

    def start_from(self, position: Coordinate):
        self.is_start = True
        self.connected_from = position - self.position
        return self

    def linked_from(self, other: 'Square') -> 'Square':
        vector = self.position - other.position
        self.connected_from = -vector
        other.connected_to.add(vector)
        return self

    def __repr__(self):
        return f'{type(self).__name__}{self.position,}'

    def __iter__(self) -> typing.Iterable[Coordinate]:
        yield from self.position

    @property
    def visited(self) -> bool:
        return hasattr(self, 'connected_from') or self.is_start

    @property
    def assigned(self) -> bool:
        return self.visited or self.is_end
