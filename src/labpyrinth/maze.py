import random

from pygame.math import Vector2

MOVES = (
    Vector2(0, 1),
    Vector2(1, 0),
    Vector2(0, -1),
    Vector2(-1, 0),
)
DIRECTIONS = '↓→↑←'
DIRECTION_LOOKUP = dict(zip([(x, y) for (x, y) in MOVES], DIRECTIONS))


class Maze:
    width: int
    height: int

    start_symbol = '😀'
    end_symbol = '🏁'

    def __init__(self, width: int, height: int):
        if width < 3 or height < 3:
            raise ValueError("Maze must be at least 3x3")
        self.width = width
        self.height = height
        self.grid = [[() for _ in range(height)] for __ in range(width)]
        self.path = {}
        self.path_from = {}
        self.start = self.end = None
        self.visited = set()
        self.solution = []

        self.creation = self._create()

    def reset(self):
        self.__init__(self.width, self.height)

    def choose_start(self):
        candidates = set()

        for i in range(self.height):
            candidates = candidates.union({(0, i), (self.width - 1, i)})

        for i in range(self.width):
            candidates = candidates.union({(i, 0), (i, self.height - 1)})

        start = (x, y) = self.start = random.choice(tuple(candidates))
        self.path[start] = self.path_from[start] = {}
        self.grid[x][y] = self.start_symbol

        self.visited.add(start)

    def choose_end(self):
        x = random.randint(1, self.width - 1)
        y = random.randint(1, self.height - 1)
        self.end = (x, y)
        self.grid[x][y] = self.end_symbol

    def _in_bounds(self, x, y):
        if (x, y) in self.visited:
            return False
        else:
            return (0 <= x < self.width) and (0 <= y < self.height)

    def _next_from(self, x: int, y: int):
        for move in MOVES:
            a, b = map(int, move + Vector2(x, y))

            if self._in_bounds(a, b):
                yield a, b, *move

    def _create(self):
        self.choose_start()
        yield self.grid
        self.choose_end()
        yield self.grid

        self.solution = path = [here := self.start]

        while here != self.end:
            x, y = here
            possible = list(self._next_from(*here))

            if not possible:
                path.pop()
                here = path[-1]
                if not self.grid[x][y]:
                    self.grid[x][y] = 'x',
                continue

            x1, y1, dx, dy = random.choice(possible)

            self.grid[x][y] = *self.grid[x][y], DIRECTION_LOOKUP[dx, dy]
            here = x1, y1
            self.visited.add(here)

            self.path_from[path[-1]][here] = self.path_from[here] = {}
            path.append(here)
            yield self.grid
