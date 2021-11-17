import random
import typing

from labpyrinth.geometry import Coordinate, Square


class Maze:
    solution: 'typing.List[Square]'
    width: int
    height: int

    def __init__(self, width: int, height: int):
        if width < 3 or height < 3:
            raise ValueError("Maze must be at least 3x3")
        self.width = width
        self.height = height
        self.grid = [[Square(Coordinate(x, y)) for y in range(height)] for x in range(width)]
        self.start = self.end = None
        self.solution = []

        self.creation = self._create()

    def __getitem__(self, position):
        x, y = position
        return self.grid[x][y]

    def reset(self):
        self.__init__(self.width, self.height)

    def choose_start(self):
        rightmost = self.width - 1
        bottommost = self.height - 1

        verticals = [
            (x, y) for x in (0, rightmost) for y in range(self.height)
        ]
        horizontals = [
            (x, y) for x in range(1, rightmost) for y in (0, bottommost)
        ]
        choice = random.choice(verticals + horizontals)
        start = self.start = self[choice]
        self.solution = [start]
        start.is_start = True

    def choose_end(self):
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)
        end = self.end = self[x, y]
        end.is_end = True

    def _in_bounds(self, coord: Coordinate):
        if (0 <= coord.x < self.width) and (0 <= coord.y < self.height):
            return not self[coord.as_tuple].visited
        return False

    def _next_from(self, position: Coordinate):
        for moved in position.neighbours():
            if (moved == self.end.position) or self._in_bounds(moved):
                yield self[moved.as_tuple]

    def _create(self):
        self.choose_start()
        yield self.grid
        self.choose_end()
        yield self.grid

        while (here := self.solution[-1]) != self.end:
            possible = list(self._next_from(here.position))

            if possible:
                choice = random.choice(possible).from_(here)

                self.solution.append(choice)

                yield self.grid
            else:
                self.solution.pop()
