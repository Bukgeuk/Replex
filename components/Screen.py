from abc import ABCMeta, abstractmethod
from typing import Tuple, final

from components.Surface import Surface


class Screen(Surface, metaclass=ABCMeta):
    def __init__(self, size: Tuple[int, int]) -> None:
        super().__init__((0, 0), size)

    def onEnterScreen(self) -> None:
        pass

    def onEscapeScreen(self) -> None:
        pass

    def onKeyDown(self, event) -> None:
        pass

    def onKeyUp(self, event) -> None:
        pass

    @abstractmethod
    def draw(self):
        pass

    @final
    def _tick(self):
        pass
