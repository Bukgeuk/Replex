import pygame.camera
from typing import List
from ..utils.position import float2d, int2d
from .Base import Component

pygame.camera.init(None)

all = ["getCameraList", "CameraCapture"]

def getCameraList() -> List[str]:
    return pygame.camera.list_cameras()

class CameraCapture(Component):
    def __init__(self, pos: float2d, size: int2d, device: str, hflip: bool = True, vflip: bool = False) -> None:
        super().__init__(pos, size)
        if device not in getCameraList():
            raise ValueError("Invalid device name")
        self.__cam = pygame.camera.Camera(device, size)
        self.__cam.start()
        self.__cam.set_controls(hflip, vflip)
        
    def setOptions(self, hflip: bool = False, vflip: bool = False):
        self.__cam.set_controls(hflip, vflip)

    @property
    def image(self):
        return self.__cam.get_image()
    
    @property
    def size(self) -> int2d:
        return self.__size
    
    def stop(self):
        self.__cam.stop()
    
