import itertools
import os
import sys

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


def create_arrow_tiles(symbols, colour: pygame.Color, transparent=COLOURS['transparent']):
    tiles = {}

    for opened in (
            opened
            for length in range(len(symbols))
            for opened in itertools.combinations(symbols, length + 1)
    ):
        if isinstance(opened, geometry.Coordinate):
            key = geometry.Direction.to_int(opened)
        else:
            key = geometry.Direction.to_int(*opened)

        rect = tiles[key] = pygame.Surface((SCALE, SCALE))
        rect.set_colorkey(transparent)
        rect.fill(transparent)

        for side in opened:
            rect.blit(
                FONT.render(symbols[side], False, colour),
                (0, 0)
            )

    return tiles


ARROW_TILES = create_arrow_tiles(
    symbols={
        geometry.Direction.down: '↓',
        geometry.Direction.right: '→',
        geometry.Direction.up: '↑',
        geometry.Direction.left: '←',
    },
    colour=COLOURS['grey']
)


def tick(display: pygame.Surface, maze_: maze.Maze, generator):
    display.fill(COLOURS['white'])
    try:
        next(generator)
    except StopIteration:
        raise
    finally:
        for (x, y) in maze_.solution:
            display.fill(COLOURS['lightgreen'], ((x * SCALE), (y * SCALE) + OFFSET, SCALE, SCALE))

        offset = pygame.Vector2(0, OFFSET)

        for square in maze_:
            position = pygame.math.Vector2(*square.position) * SCALE
            position += offset

            if square.is_start:
                display.blit(FONT.render('😀', True, COLOURS['red']), position)
            if square.is_end:
                display.blit(FONT.render('🏁', True, COLOURS['red']), position)
            elif key := geometry.Direction.to_int(*square.open_sides()):
                display.blit(ARROW_TILES[key], position)


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
            _tick(display, maze_, generator)
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
