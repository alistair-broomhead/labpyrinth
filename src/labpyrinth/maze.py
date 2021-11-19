import random
import typing

from labpyrinth.geometry import Coordinate, Square


class Maze:
    width: int
    height: int
    solution: typing.List[Square]

    _grid: typing.Dict[Coordinate, Square]
    _generator: typing.Iterable[typing.Tuple[Square]]

    def __init__(self, width: int, height: int):
        if width < 3 or height < 3:
            raise ValueError("Maze must be at least 3x3")
        self.width = width
        self.height = height

        self.all_positions = frozenset(
            Coordinate(x, y) for x in range(width) for y in range(height)
        )
        self.inside = list(inside := {
            coord for coord in self.all_positions
            if (coord.x not in {0, width - 1}) and (coord.y not in {0, height - 1})
        })
        self.circumference = list(self.all_positions - inside)
        self.reset()

    def __iter__(self):
        while True:
            yield next(self._generator)

    def __getitem__(self, position):
        x, y = position
        return self._grid[Coordinate(x, y)]

    def reset(self):
        self._grid = {
            coord: Square(coord) for coord in self.all_positions
        }
        self.solution = []

        self._generator = self.create()

    def choose_start(self):
        choice = random.choice(self.circumference)
        self.solution = [start := self[choice]]

        for neighbour in start.neighbour_positions():
            if not self._in_bounds(neighbour):
                return start.start_from(neighbour)

    def choose_end(self):
        end = self[random.choice([
            Coordinate(x, y)
            for x in range(self.width // 4, 3 * self.width // 4)
            for y in range(self.height // 4, 3 * self.width // 4)
        ])]
        end.is_end = True
        return end

    def _in_bounds(self, coord: Coordinate) -> bool:
        return (0 <= coord.x < self.width) and (0 <= coord.y < self.height)

    def _neighbours(self, square: Square):
        yield from (
            self[coord] for coord in
            filter(self._in_bounds, square.neighbour_positions())
        )

    @staticmethod
    def _next(steps: typing.List[Square], here: Square, possible: typing.List[Square]):
        yield here

        if possible:
            steps.append(
                there := random.choice(possible).linked_from(here)
            )
            yield there
        else:
            steps.remove(here)

    def create(self):
        yield self.choose_start(),
        yield self.choose_end(),

        while not (here := self.solution[-1]).is_end:
            yield self._next(self.solution, here, [
                square for square in self._neighbours(here)
                if not square.visited  # Allow selecting the end
            ])

        # We don't want a continuation from the end
        remainder = self.solution[:-1]

        while remainder:
            # This encourages having a grater number of, albeit
            # shorter, incorrect paths
            end = remainder[-1]
            here = random.choice(remainder)
            here = random.choice((here, end))
            yield self._next(remainder, here, [
                square for square in self._neighbours(here)
                if not square.assigned  # Don't select the end
            ])

        while True:
            yield ()
