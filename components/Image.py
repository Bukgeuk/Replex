from __future__ import annotations

from typing import Tuple

import pygame

from components.Base import InteractiveDisplayObject


class Image(InteractiveDisplayObject):
    def __init__(self, path: str, pos: Tuple[int, int] = (0, 0)) -> None:
        self.__image: pygame.surface.Surface = pygame.image.load(path)
        super().__init__(pos, self.__image.get_size())

    def getPygameImage(self) -> pygame.surface.Surface:
        return self.__image

    def rescale(self, size: Tuple[int, int]) -> Image:
        self.__image = pygame.transform.scale(self.__image, size)
        self.setSize(size)
        return self