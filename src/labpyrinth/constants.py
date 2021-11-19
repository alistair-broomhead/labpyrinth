import pygame

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
SCALE = 60
OFFSET = 0
