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

    def _neighbours(self, square: Square):
        for coord in square.position.neighbours():
            if (0 <= coord.x < self.width) and (0 <= coord.y < self.height):
                yield self._grid[coord]

    @staticmethod
    def _next(steps: typing.List[Square], here: Square, possible: typing.List[Square]):
        if possible:
            steps.append(
                random.choice(possible).from_(here)
            )
        else:
            steps.remove(here)

    def create(self):
        yield self.choose_start()
        yield self.choose_end()

        while not (here := self.solution[-1]).is_end:
            self._next(self.solution, here, [
                square for square in self._neighbours(here)
                if not square.visited  # Allow selecting the end
            ])
            yield

        # We don't want a continuation from the end
        remainder = self.solution[:-1]

        while remainder:
            # This encourages having a grater number of shorter
            # incorrect paths
            here = random.choice(remainder)
            self._next(remainder, here, [
                square for square in self._neighbours(here)
                if not square.assigned  # Don't select the end
            ])
            yield
