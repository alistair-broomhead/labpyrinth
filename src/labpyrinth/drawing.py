import typing

import pygame

from labpyrinth import constants, geometry, maze


def show_fps(
        display: pygame.Surface,
        clock: pygame.time.Clock,
        location: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
):
    display.fill(constants.COLOURS['grey'], (0, 0, display.get_width(), constants.OFFSET))
    info = (
        f'{clock.get_fps() :0.0f} FPS    '
        f'Frame = {clock.get_time()} ms    '
        f'Render = {clock.get_rawtime()} ms'
    )
    display.blit(constants.FONT.render(info, False, constants.COLOURS['black']), location)


def blit_centre(onto: pygame.Surface, blit: pygame.Surface):
    x = onto.get_width() - blit.get_width()
    y = onto.get_height() - blit.get_height()
    onto.blit(blit, (x / 2, y / 2))
    return onto


def wall_tiles(colour: pygame.Color = constants.COLOURS['black']):
    d = geometry.Direction
    tiles = {}

    wall_thickness = constants.SCALE // 8
    end_offset = constants.SCALE - wall_thickness

    lookup = {
        d.up: (0, 0, constants.SCALE, wall_thickness),
        d.down: (0, end_offset, constants.SCALE, wall_thickness),
        d.left: (0, 0, wall_thickness, constants.SCALE),
        d.right: (end_offset, 0, wall_thickness, constants.SCALE),
    }

    for closed in d.combinations():
        rect = tiles[d.to_int(*closed)] = transparent_tile()

        for side in closed:
            rect.fill(colour, lookup[side])

    return tiles


def grid_to_coord(position: typing.Union[tuple, pygame.math.Vector2, geometry.Coordinate]) -> pygame.math.Vector2:
    if not isinstance(position, pygame.math.Vector2):
        position = pygame.Vector2(*position)

    return (position * constants.SCALE) + pygame.Vector2(0, constants.OFFSET)


def tile(colour: pygame.Color) -> pygame.Surface:
    t = pygame.Surface((constants.SCALE, constants.SCALE))
    t.fill(colour)
    return t


def transparent_tile():
    rect = tile(constants.COLOURS['transparent'])
    rect.set_colorkey(constants.COLOURS['transparent'])

    return rect


class _Tiles:
    def __init__(self):
        self.visited = tile(constants.COLOURS['lightgreen'])
        self.blank = tile(constants.COLOURS['white'])
        self.start = tile(constants.COLOURS['green'])
        self.goal = blit_centre(
            tile(constants.COLOURS['green']),
            constants.FONT.render('🏁', True, constants.COLOURS['black'])
        )
        self.walls = wall_tiles()

    def __call__(self):
        self.__init__()


TILES = _Tiles()


def draw_square(
        display: pygame.Surface,
        maze_: maze.Maze,
        debug: bool,
        square: geometry.Square
):
    position = grid_to_coord(square.position)

    if debug:
        if square.is_start or square.is_end:
            display.blit(TILES.start, position)
        else:
            display.blit(TILES.visited, position)
    else:
        display.blit(TILES.blank, position)

    if key := geometry.Direction.to_int(*square.closed_sides()):
        display.blit(TILES.walls[key], position)


def clear_display(display):
    display.fill(constants.COLOURS['white'])
    return display
