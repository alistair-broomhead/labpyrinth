"""
Labpyrinth is a python application which generates mazes
"""

import os
import sys

import pygame

pygame.init()
pygame.display.set_caption('Labpyrinth')

# pylint: disable=wrong-import-position
from labpyrinth import (
    constants,
    drawing,
    events,
    geometry,
    maze,
)


@events.Handle(type=pygame.QUIT)
@events.Handle(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
@events.Handle(type=pygame.KEYDOWN, key=pygame.K_q)
def quit_game(_):
    """ On any of these events, quit instantly """
    raise SystemExit


class Main:
    columns, rows = 12, 12

    def __init__(self, width: int = 800, height: int = 600, debug=False):
        self.debug = debug
        self._reset = False

        self.maze = maze.Maze(
            width=self.columns,
            height=self.rows,
        )

        available_height = height - constants.OFFSET
        col_width = width // self.columns
        row_height = available_height // self.rows

        scale = constants.SCALE = min(col_width, row_height)
        drawing.TILES()

        height = (self.rows * scale) + constants.OFFSET
        width = self.columns * scale

        self.clock = pygame.time.Clock()
        self.display = drawing.clear_display(
            pygame.display.set_mode((width, height))
        )

    def reset(self, _=None):
        self._reset = True

    def _create_maze(self):
        drawing.clear_display(self.display)
        self.maze.reset()

        for squares in self.maze.create():
            if self._reset:
                return

            for square in squares:
                drawing.draw_square(self.display, self.maze, self.debug, square)

            self._frame()

    def _idle(self):
        while not self._reset:
            self._frame()

    def _frame(self):
        if self.debug:
            drawing.show_fps(self.display, self.clock)

        pygame.display.update()

        events.Handle.handle_events()

        self.clock.tick(100)

        return self._reset

    def run(self):
        events.Handle.assign(self.reset, type=pygame.KEYDOWN, key=pygame.K_r)

        while True:
            self._reset = False
            self._create_maze()
            self._idle()


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
        Main(**KWARGS).run()
    finally:
        pygame.quit()
