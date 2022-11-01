from optparse import Option
import pygame
from typing import Optional, Dict

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