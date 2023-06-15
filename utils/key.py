import pygame

__all__ = ['getKeyFocused', 'getKeyState', 'getModifierKeyState', 'isModifierKeyStateContain', 'getKeyCodeByString']

def getKeyFocused():
    return pygame.key.get_focused()

def getKeyState():
    return pygame.key.get_pressed()

def getModifierKeyState():
    return pygame.key.get_mods()

def isModifierKeyStateContain(state, target) -> bool:
    '''
    * state: event.mod or getModifierKeyState()
    * target: pygame.{KEY}
    '''
    return bool(state & target)

def getKeyCodeByString(string: str) -> int:
    return pygame.key.key_code(string)