"""
Labpyrinth is a python application which generates mazes
"""

import os
import sys

import pygame

pygame.init()

# pylint: disable=wrong-import-position
from labpyrinth import (
    constants,
    drawing,
    events,
    geometry,
    maze,
)


def main(width: int = 600, height: int = 600, debug=False):
    """ Event loop """
    pygame.display.set_caption('Labpyrinth')
    display = pygame.display.set_mode((width, height + constants.OFFSET))
    display.fill(constants.COLOURS['white'])

    clock = pygame.time.Clock()

    maze_ = maze.Maze(width=width // constants.SCALE, height=height // constants.SCALE)

    @events.Handle(type=pygame.KEYDOWN, key=pygame.K_r)
    def reset(_):
        maze_.reset()
        drawing.clear_display(display)

    for squares in maze_:
        clock.tick(100)

        if debug:
            drawing.show_fps(display, clock)

        for square in squares:
            drawing.draw_square(display, maze_, debug, square)

        pygame.display.update()

        events.Handle.handle_events()


def is_debug():
    """
    If DEBUG is set to something truthy in the environment,
    or this is run in a debugger, we can enable debug
    functionality.
    """
    # Check environment
    if os.environ.get('DEBUG', False):
        return True

    # Detect whether we are running within a debugger
    debugger = getattr(sys, 'gettrace', lambda: None)()
    return debugger is not None


if __name__ == "__main__":
    KWARGS = {}

    if is_debug():
        constants.OFFSET = constants.FONT_HEIGHT
        KWARGS['debug'] = True

    try:
        main(**KWARGS)
    finally:
        pygame.quit()
