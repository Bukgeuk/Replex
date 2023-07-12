import pygame.camera
from typing import List
from ..utils.position import Pos
from .Base import Component

pygame.camera.init()

all = ["getCameraList", "Camera"]

def getCameraList() -> List[str]:
    return pygame.camera.list_cameras()

class Camera(Component):
    def __init__(self, pos: Pos, size: Pos, device: str, hflip: bool = False, vflip: bool = False) -> None:
        super().__init__(pos, size)
        self.__cam = pygame.camera.Camera(device, size)
        self.__cam.start()
        self.__cam.set_controls(hflip, vflip)
        
    def setOptions(self, hflip: bool = False, vflip: bool = False):
        self.__cam.set_controls(hflip, vflip)

    @property
    def image(self):
        return self.__cam.get_image()
    
    @property
    def size(self) -> Pos:
        return self.__size
    
    def stop(self):
        self.__cam.stop()
    
