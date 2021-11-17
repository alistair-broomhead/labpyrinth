import os
import sys

import pygame

from labpyrinth.maze import Maze

pygame.init()

SCALE = 32

COLOURS = {
    'black': pygame.color.Color(0x00, 0x00, 0x00),
    'white': pygame.color.Color(0xff, 0xff, 0xff),
    'grey': pygame.color.Color(0x88, 0x88, 0x88),
    'green': pygame.color.Color(0x88, 0xff, 0x88),
}
FONT = pygame.font.SysFont('segoeuiemoji', 16)
FONT_HEIGHT = FONT.get_height()
OFFSET = 0


def blit_text(
        display: pygame.Surface,
        text: str,
        location: pygame.math.Vector2,
        antialias: bool = True,
        colour: pygame.color.Color = COLOURS['black'],
        font: pygame.font.Font = FONT,
):
    location.y += OFFSET
    display.blit(font.render(text, antialias, colour), location)


def blit_path(display, x, y):
    display.fill(COLOURS['green'], ((x * SCALE), (y * SCALE) + OFFSET, SCALE, SCALE))


def show_fps(
        display: pygame.Surface,
        clock: pygame.time.Clock,
        location: pygame.math.Vector2 = pygame.math.Vector2(0, 0),
        **kwargs
):
    location.y -= OFFSET
    display.fill(COLOURS['grey'], (0, 0, display.get_width(), OFFSET))
    info = f'{clock.get_fps():0.0f} FPS    Frame = {clock.get_time()} ms    Render = {clock.get_rawtime()} ms'
    blit_text(display, info, location, **kwargs)


def no_tick(*_, **__):
    pass


def tick(display: pygame.Surface, maze_: Maze):
    print("tick!")
    display.fill(COLOURS['white'])
    try:
        next(maze_.creation)
    except StopIteration:
        raise
    finally:
        for (x, y) in maze_.solution:
            blit_path(display, x, y)

        for x, column in enumerate(maze_.grid):
            for y, square in enumerate(column):
                for char in square.symbols:
                    blit_text(display, char, pygame.math.Vector2(SCALE * x, SCALE * y))


def main(width: int = 640, height: int = 480, debug=False):
    pygame.display.set_caption('Labpyrinth')
    display = pygame.display.set_mode((width, height + OFFSET))
    display.fill(COLOURS['white'])

    clock = pygame.time.Clock()

    maze_ = Maze(width=width // SCALE, height=height // SCALE)

    _tick = tick

    while True:
        clock.tick(100)
        try:
            _tick(display, maze_)
        except StopIteration:
            _tick = no_tick

        if debug:
            show_fps(display, clock)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                maze_.reset()
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

    main(**KWARGS)
