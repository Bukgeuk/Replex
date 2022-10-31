from xmlrpc.client import Boolean
import pygame

def getMousePressed():
    '''Please use this in MouseDown, MouseUp or MouseMove event'''
    return pygame.mouse.get_pressed()

def getMousePos():
    return pygame.mouse.get_pos()

def setMousePos(x: float, y: float):
    pygame.mouse.set_pos(x, y)

def setMouseVisible(value: Boolean):
    pygame.mouse.set_visible(value)

def getMouseVisible() -> Boolean:
    return pygame.mouse.get_visible()

def getMouseFocused():
    return pygame.mouse.get_focused()
