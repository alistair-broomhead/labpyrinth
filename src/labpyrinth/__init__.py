import os
import sys
import typing

import pygame

from labpyrinth import maze, geometry

pygame.init()

SCALE = 32

COLOURS = {
    # We'll use this shade of purple as a colour key
    # for transparency, more efficient than alpha channel
    'transparent': pygame.color.Color(0xf0, 0x0f, 0xf0),

    'black': pygame.color.Color(0x00, 0x00, 0x00),
    'white': pygame.color.Color(0xff, 0xff, 0xff),
    'grey': pygame.color.Color(0x88, 0x88, 0x88),
    'lightgreen': pygame.color.Color(0x88, 0xff, 0x88),
    'green': pygame.color.Color(0x00, 0xff, 0x00),
    'red': pygame.color.Color(0xff, 0x00, 0x00),
}
FONT = pygame.font.SysFont('segoeuiemoji', 16)
FONT_HEIGHT = FONT.get_height()
OFFSET = 0


def show_fps(
        display: pygame.Surface,
        clock: pygame.time.Clock,
        location: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
):
    display.fill(COLOURS['grey'], (0, 0, display.get_width(), OFFSET))
    info = f'{clock.get_fps():0.0f} FPS    Frame = {clock.get_time()} ms    Render = {clock.get_rawtime()} ms'
    display.blit(FONT.render(info, False, COLOURS['black']), location)


def no_tick(*_, **__):
    pass


def transparent_tile():
    rect = pygame.Surface((SCALE, SCALE))
    rect.set_colorkey(COLOURS['transparent'])
    rect.fill(COLOURS['transparent'])

    return rect


def blit_centre(onto: pygame.Surface, blit: pygame.Surface):
    x = onto.get_width() - blit.get_width()
    y = onto.get_height() - blit.get_height()
    onto.blit(blit, (x / 2, y / 2))
    return onto


def arrow_tiles(symbols, colour: pygame.Color):
    d = geometry.Direction
    tiles = {}

    for opened in d.combinations():
        rect = tiles[d.to_int(*opened)] = transparent_tile()

        for side in opened:
            blit_centre(
                onto=rect,
                blit=FONT.render(symbols[side], False, colour)
            )

    return tiles


ARROW_TILES = arrow_tiles(
    symbols={
        geometry.Direction.down: '↓',
        geometry.Direction.right: '→',
        geometry.Direction.up: '↑',
        geometry.Direction.left: '←',
    },
    colour=COLOURS['grey']
)


def wall_tiles(colour: pygame.Color):
    d = geometry.Direction
    tiles = {}

    wall_thickness = SCALE // 8
    end_offset = SCALE - wall_thickness

    lookup = {
        d.up: (0, 0, SCALE, wall_thickness),
        d.down: (0, end_offset, SCALE, wall_thickness),
        d.left: (0, 0, wall_thickness, SCALE),
        d.right: (end_offset, 0, wall_thickness, SCALE),
    }

    for closed in d.combinations():
        rect = tiles[d.to_int(*closed)] = transparent_tile()

        for side in closed:
            rect.fill(colour, lookup[side])

    return tiles


WALL_TILES = wall_tiles(
    colour=COLOURS['black']
)


def _grid_to_coord(position: typing.Union[tuple, pygame.math.Vector2, geometry.Coordinate]) -> pygame.math.Vector2:
    if not isinstance(position, pygame.math.Vector2):
        position = pygame.Vector2(*position)

    return (position * SCALE) + pygame.Vector2(0, OFFSET)


VISITED = pygame.Surface((SCALE, SCALE))
VISITED.fill(COLOURS['lightgreen'])
BLANK = pygame.Surface((SCALE, SCALE))
BLANK.fill(COLOURS['white'])


def tick(display: pygame.Surface, maze_: maze.Maze, debug: bool, generator):
    d = geometry.Direction

    try:
        squares = next(generator)
    except StopIteration:
        raise

    visited = {square.position for square in maze_.solution}

    for square in squares:
        if square is None:
            continue

        position = _grid_to_coord(square.position)

        clear = VISITED if debug and square.position in visited else BLANK
        display.blit(clear, position)

        if square.is_start:
            display.fill(COLOURS['green'], (*position, SCALE, SCALE))

        if square.is_end:
            goal = pygame.Surface((SCALE, SCALE))
            goal.fill(COLOURS['green'])

            display.blit(
                blit_centre(goal, FONT.render('🏁', True, COLOURS['black'])),
                position
            )

        if key := d.to_int(*square.closed_sides()):
            display.blit(WALL_TILES[key], position)


def main(width: int = 640, height: int = 480, debug=False):
    pygame.display.set_caption('Labpyrinth')
    display = pygame.display.set_mode((width, height + OFFSET))
    display.fill(COLOURS['white'])

    clock = pygame.time.Clock()

    maze_ = maze.Maze(width=width // SCALE, height=height // SCALE)
    generator = maze_.create()

    _tick = tick

    while True:
        clock.tick(100)
        try:
            _tick(display, maze_, debug, generator)
        except StopIteration:
            # Prevent redrawing when there's no changes
            _tick = no_tick

        if debug:
            show_fps(display, clock)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    maze_.reset()
                    generator = maze_.create()
                    display.fill(COLOURS['white'])
                    _tick = tick


def is_debug():
    # Check environment
    if os.environ.get('DEBUG', False):
        return True

    # Detect whether we are running within a debugger
    debugger = getattr(sys, 'gettrace', lambda: None)()
    return debugger is not None


if __name__ == "__main__":
    KWARGS = {}

    if is_debug():
        OFFSET = FONT.get_height()
        KWARGS['debug'] = True

    try:
        main(**KWARGS)
    finally:
        pygame.quit()
