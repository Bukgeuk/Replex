from abc import ABCMeta, abstractmethod

from .Surface import Surface
from .Base import Pos


class Screen(Surface, metaclass=ABCMeta):
    def __init__(self, size: Pos) -> None:
        super().__init__((0, 0), size)

    def onEnterScreen(self) -> None:
        pass

    def onEscapeScreen(self) -> None:
        pass

    @abstractmethod
    def draw(self):
        pass

    def tick(self):
        super().tick()
