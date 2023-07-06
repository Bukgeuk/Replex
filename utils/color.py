from __future__ import annotations
from typing import Union, Tuple

__all__ = ['ColorLike', 'Color', 'COLORS']

ColorLike = Union[Tuple[int, int, int], Tuple[int, int, int, int], str]
class Color:
    def __init__(self, color: ColorLike) -> None:
        if type(color) is tuple:
            self.__r = color[0]
            self.__g = color[1]
            self.__b = color[2]
            self.__a =  1 if len(color) < 4 else color[3]
        elif type(color) is str:
            rgba = self.HEXToRGBA(color)
            self.__r = rgba[0]
            self.__g = rgba[1]
            self.__b = rgba[2]
            self.__a = rgba[3]

    @property
    def rgba(self) -> Tuple[int, int, int, int]:
        return (self.__r, self.__g, self.__b, self.__a)
    
    @property
    def hex(self) -> str:
        return self.RGBAToHEX(self.rgba)

    @staticmethod
    def HEXToRGBA(hex: str) -> Tuple[int, int, int, int]:
        code = hex.lstrip('#')
        if len(code) == 6:
            code += 'FF'
        elif len(code) != 8:
            raise ValueError(f"'{hex}' is not a valid hex color.")

        return tuple(int(code[i:i+2], 16) for i in (0, 2, 4, 6))
    
    @staticmethod
    def RGBAToHEX(rgba: Tuple[int, int, int, int]) -> str:
        code = '%02x%02x%02x%02x' % rgba
        return '#' + code
    
    @staticmethod
    def RGBToHEX(rgb: Tuple[int, int, int]) -> str:
        code = '%02x%02x%02x' % rgb
        return '#' + code

class _COLORS:
    @property
    def BLACK(self):
        return Color((0, 0, 0))
    
    @property
    def WHITE(self):
        return Color((255, 255, 255))
    
    @property
    def RED(self):
        return Color((255, 0, 0))
    
    @property
    def ORANGE(self):
        return Color((255, 128, 0))
    
    @property
    def YELLOW(self):
        return Color((255, 255, 0))
    
    @property
    def GREEN(self):
        return Color((0, 255, 0))
    
    @property
    def SKYBLUE(self):
        return Color((0, 128, 255))
    
    @property
    def BLUE(self):
        return Color((0, 0, 255))
    
    @property
    def PURPLE(self):
        return Color((127, 0, 255))
    
    @property
    def PINK(self):
        return Color((255, 0, 255))
    
    @property
    def HOTPINK(self):
        return Color((255, 0, 127))
    
    @property
    def GRAY(self):
        return Color((128, 128, 128))
    
COLORS = _COLORS()