from typing import Dict, Optional, Tuple

import pygame

from components.Image import Image

__fontStorage: Dict[str, pygame.font.Font] = {}

def loadSystemFont(name: str, size: int, bold: bool = False, italic: bool = False, regName: Optional[str] = None) -> pygame.font.Font:
    '''
    if regName is None, font is stored as name
    '''
    font = pygame.font.SysFont(name, size, bold, italic)
    if regName is None:
        regName = name
    __fontStorage[regName] = font

    return font

def loadFont(path: str, size: int, regName: Optional[str] = None) -> pygame.font.Font:
    '''
    if regName is None, font is stored as path
    '''
    font = pygame.font.Font(path, size)
    if regName is None:
        regName = path
    __fontStorage[regName] = font

    return font

def getFont(regName: str) -> Optional[pygame.font.Font]:
    return __fontStorage[regName] if regName in __fontStorage else None

def textToImageByFont(text: str, font: pygame.font.Font, color: Tuple[int, int, int], antialias: bool = True) -> Image:
    image = font.render(text, antialias, color)
    return Image(_pygameSurface=image)

def textToImageByFontName(text: str, fontName: str, color: Tuple[int, int, int], antialias: bool = True) -> Optional[Image]:
    font = getFont(fontName)
    print(__fontStorage)
    return textToImageByFont(text, font, color, antialias) if font is not None else None
