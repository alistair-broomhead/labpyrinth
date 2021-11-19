import typing

import pygame


class Handle:
    _handled: typing.List[
        typing.Tuple[
            typing.Dict[str, typing.Any], typing.Callable
        ]
    ] = []

    def __init__(self, **conditions):
        self.conditions = conditions

    def __call__(self, handler):
        self._handled.append((self.conditions, handler))
        return handler

    @classmethod
    def _handle(cls, event: pygame.event.Event):
        for conditions, handler in cls._handled:
            if all(
                    getattr(event, attr, None) == value
                    for attr, value in conditions.items()
            ):
                handler(event)

    @classmethod
    def handle_events(cls):
        for event in pygame.event.get():
            cls._handle(event)


@Handle(type=pygame.QUIT)
@Handle(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
@Handle(type=pygame.KEYDOWN, key=pygame.K_q)
def quit_game(_):
    raise SystemExit
