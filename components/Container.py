from abc import ABCMeta, abstractmethod

from .Surface import Surface
from .Scene import Scene
from .Base import int2d

__all__ = ['Container']

class Container(Surface, metaclass=ABCMeta):
    def __init__(self, size: int2d) -> None:
        super().__init__((0, 0), size)

    @abstractmethod
    def draw(self):
        pass

    def tick(self):
        super().tick()
