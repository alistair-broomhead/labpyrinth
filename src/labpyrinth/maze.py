import random


class Coordinate:
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

    def __add__(self, other):
        x, y = other

        return type(self)(self.x + x, self.y + y)

    def __sub__(self, other):
        x, y = other

        return self + (-x, -y)


MOVES = (
    (Coordinate(0, 1), '↓'),
    (Coordinate(1, 0), '→'),
    (Coordinate(0, -1), '↑'),
    (Coordinate(-1, 0), '←'),
)


class Square:
    def __init__(self, position: Coordinate):
        self.position = position
        self.symbols = ()

    def __repr__(self):
        return f'{type(self).__name__}{self.position.as_tuple + self.symbols}'

    def __hash__(self):
        return hash((type(self), *self))

    def __iter__(self):
        yield from self.position.as_tuple

    @property
    def visited(self):
        return bool(self.symbols)

    def add(self, symbol: str):
        self.symbols = *self.symbols, symbol
        return self


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
        self.grid = [[Square(Coordinate(x, y)) for y in range(height)] for x in range(width)]
        self.path = {}
        self.path_from = {}
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
        start = self.start = self[choice].add(self.start_symbol)
        self.solution = [start]
        self.path[start] = self.path_from[start] = {}

    def choose_end(self):
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)
        self.end = self[x, y].add(self.end_symbol)

    def _in_bounds(self, coord: Coordinate):
        if (0 <= coord.x < self.width) and (0 <= coord.y < self.height):
            return not self[coord.as_tuple].visited
        return False

    def _next_from(self, x: int, y: int):
        for move, symbol in MOVES:
            moved = (Coordinate(x, y) + move)
            if (moved == self.end.position) or self._in_bounds(moved):
                yield self[moved.as_tuple], symbol

    def _create(self):
        self.choose_start()
        yield self.grid
        self.choose_end()
        yield self.grid

        while self.solution[-1] != self.end:
            x, y = here = self.solution[-1]
            to_go = self.end.position - here.position

            possible = list(self._next_from(x, y))

            if possible:
                choice, symbol = random.choice(possible)

                self[here].add(symbol)

                self.path_from[here][choice] = self.path_from[choice] = {}
                self.solution.append(choice)

                yield self.grid
            else:
                self.solution.pop()

                if not self[here].symbols:
                    self[here].add('x')
