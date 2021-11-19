""" Simplify pygame event handling """

import typing

import pygame


class Handle:
    """ Decorator used to create handler functions """
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
    def assign(cls, handler, **conditions):
        """ Non-decorator invocation """
        return cls(**conditions)(handler)

    @classmethod
    def _handle(cls, event: pygame.event.Event):
        """ Handle a single event """
        for conditions, handler in cls._handled:
            if all(
                    getattr(event, attr, None) == value
                    for attr, value in conditions.items()
            ):
                handler(event)

    @classmethod
    def handle_events(cls):
        """ Handle all the pygame events from the last tick """
        for event in pygame.event.get():
            cls._handle(event)
