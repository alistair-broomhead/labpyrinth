import os
import sys

import pygame

pygame.init()

COLOURS = {
    'black': pygame.color.Color(0x00, 0x00, 0x00),
    'white': pygame.color.Color(0xff, 0xff, 0xff),
}
FONT = pygame.font.SysFont('consolas', 16)


def show_fps(
        display: pygame.Surface,
        clock: pygame.time.Clock,
        antialias: bool = True,
        colour: pygame.color.Color = COLOURS['black'],
        font: pygame.font.Font = FONT,
        location: pygame.math.Vector2 = pygame.math.Vector2(0, 0),
):
    img = font.render(
        f'{clock.get_fps():0.0f} FPS    Frame = {clock.get_time()} ms    Render = {clock.get_rawtime()} ms',
        antialias,
        colour,
    )
    display.blit(img, location)


def tick(display: pygame.Surface):
    display.fill(COLOURS['white'])


def main(width: int = 800, height: int = 600, debug=False):
    pygame.display.set_caption('Labpyrinth')
    display = pygame.display.set_mode((width, height))
    display.fill(COLOURS['white'])

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        tick(display)
        if debug:
            show_fps(display, clock)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def is_debug():
    # Check environment
    if os.environ.get('DEBUG', False):
        return True

    # Detect whether we are running within a debugger
    debugger = getattr(sys, 'gettrace', lambda: None)()
    return debugger is not None


if __name__ == "__main__":
    main(debug=is_debug())
