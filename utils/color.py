from __future__ import annotations
from typing import Union, Tuple

__all__ = ['ColorLike', 'Color', 'BLACK', 'WHITE']

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
    
BLACK = Color((0, 0, 0))
WHITE = Color((255, 255, 255))
    
