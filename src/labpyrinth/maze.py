""" See comment on Maze class """

import random
import typing

from labpyrinth.geometry import Coordinate, Square


class Maze:
    """
    This is where the magic happens. Create a Maze object,
    call Maze.create() and by the time you've iterated through
    everything it spits out, you've got you a maze!
    """
    width: int
    height: int
    solution: typing.List[Square]

    _grid: typing.Dict[Coordinate, Square]
    _generator: typing.Iterable[typing.Tuple[Square]]

    def __init__(self, width: int, height: int):
        if width < 9 or height < 9:
            raise ValueError("Maze must be at least 9x9")
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

    def __getitem__(self, position):
        if not isinstance(position, Coordinate):
            position = Coordinate(*position)
        return self._grid[position]

    def reset(self):
        """ Reset all mutated state so we can start over """
        self._grid = {
            coord: Square(coord) for coord in self.all_positions
        }
        self.solution = []

    def choose_start(self) -> typing.Iterable[Square]:
        """ Choose an edge square to start from """
        choice = random.choice(self.circumference)
        self.solution = [start := self[choice]]
        # We must have come from outside of the maze
        external_neighbours = filter(
            self._out_of_bounds,
            start.neighbour_positions()
        )
        # There can only be exactly one or two external
        # neighbours (two requires that the start position
        # is on a corner) but we'll just take the first
        # pylint: disable=stop-iteration-return
        neighbour = next(external_neighbours)

        yield start.start_from(neighbour)

    def choose_end(self) -> typing.Iterable[Square]:
        """
        Choose where the 3x3 goal square goes

        We make sure there are at least 2 tiles between the
        goal and the outside of the maze, to improve the
        chances of an interestingly long path for the
        solution.

        """
        goal_centre = random.choice([
            Coordinate(x, y)
            for x in range(4, self.width - 3)
            for y in range(4, self.width - 3)
        ])

        goal_squares = {
            self[coord] for coord in (
                goal_centre + (x, y)
                for x in range(-1, 2)
                for y in range(-1, 2)
            )
        }

        for square in goal_squares:
            square.is_end = True
            for neighbour in self._neighbours(square):
                if neighbour in goal_squares:
                    square.connected_to.add(square.vector_to(neighbour))
            yield square

    def _in_bounds(self, coord: Coordinate) -> bool:
        return (0 <= coord.x < self.width) and (0 <= coord.y < self.height)

    def _out_of_bounds(self, coord: Coordinate) -> bool:
        return not self._in_bounds(coord)

    def _neighbours(self, square: Square) -> typing.Iterable[Square]:
        yield from (
            self[coord] for coord in
            filter(self._in_bounds, square.neighbour_positions())
        )

    def _next(
            self,
            here: Square,
            steps: typing.List[Square],
            possible: typing.List[Square]
    ) -> typing.Iterable[Square]:
        """
        Find the next step on a path, starting from here

        Steps is a list of places we've visited, while possible
        is a list of possible next steps. If there's nowhere to
        go then we'll need to backtrack, removing our newly
        discovered dead-end from the list of places we might
        wish to return to.

        We always yield the squares which are affected by the
        changes we have made to the maze state, so that we can
        re-render them in their new state.
        """
        if possible:
            steps.append(
                there := random.choice(possible).linked_from(here)
            )
            yield there
            yield from (
                neighbor for neighbor in self._neighbours(there)
                if neighbor.assigned
            )
        else:
            steps.remove(here)
            yield here

    def create(self) -> typing.Iterable[typing.Iterable[Square]]:
        """
        Generates the maze, one square at a time.

        Yields a tuple of all squares that have been updated
        so that they can be rendered.
        """
        yield self.choose_start()
        yield self.choose_end()

        while not (here := self.solution[-1]).is_end:
            yield self._next(here, self.solution, [
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
            yield self._next(here, remainder, [
                square for square in self._neighbours(here)
                if not square.assigned  # Don't select the end
            ])
