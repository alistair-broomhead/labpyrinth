import random
import typing

from labpyrinth.geometry import Coordinate, Square


class Maze:
    width: int
    height: int
    solution: typing.List[Square]

    _grid: typing.Dict[Coordinate, Square]

    def __init__(self, width: int, height: int):
        if width < 3 or height < 3:
            raise ValueError("Maze must be at least 3x3")
        self.width = width
        self.height = height

        self.all_positions = {
            Coordinate(x, y) for x in range(width) for y in range(height)
        }
        self.inside = list(inside := {
            coord for coord in self.all_positions
            if (coord.x not in {0, width - 1}) and (coord.y not in {0, height - 1})
        })
        self.circumference = list(self.all_positions - inside)

        self.reset()

    def __iter__(self):
        yield from self._grid.values()

    def __getitem__(self, position):
        x, y = position
        return self._grid[Coordinate(x, y)]

    def reset(self):
        self._grid = {
            coord: Square(coord) for coord in self.all_positions
        }
        self.solution = []

    def choose_start(self):
        choice = random.choice(self.circumference)
        self.solution = [start := self[choice]]
        start.is_start = True

    def choose_end(self):
        choice = random.choice(self.inside)
        self[choice].is_end = True

    def _in_bounds(self, coord: Coordinate):
        if (0 <= coord.x < self.width) and (0 <= coord.y < self.height):
            return not self[coord.as_tuple].visited
        return False

    def _next_from(self, position: Coordinate):
        for moved in position.neighbours():
            if self._in_bounds(moved) and not self[moved].visited:
                yield self[moved]

    def create(self):
        yield self.choose_start()
        yield self.choose_end()

        while not (here := self.solution[-1]).is_end:
            possible = [
                self[moved] for moved in here.position.neighbours()
                if self._in_bounds(moved) and not self[moved].visited
            ]

            if possible:
                self.solution.append(
                    random.choice(possible).from_(here)
                )
            else:
                self.solution.pop()

            yield
