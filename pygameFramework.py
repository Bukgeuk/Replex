from __future__ import annotations
from enum import Enum
from xmlrpc.client import Boolean
import pygame, sys
from typing import Callable, Dict, List

from components.Screen import Screen
import api.key, api.mouse

class EventType(Enum):
    INIT = 0
    QUIT = 1

class DisplayMode(Enum):
    WINDOWED = 0
    FULLSCREEN = 1
    NOFRAME = 2
    HIDDEN = 3

class App:
    def __init__(self, initialScreen) -> None:
        pygame.init()

        self.__terminate = False
        self.__clock = pygame.time.Clock()
        self.__framerate: int = 0
        self.__eventListeners: Dict[EventType, List[Callable[[App], None]]] = {}
        self.__screen: Screen = initialScreen

    def __occurEvent(self, event: EventType) -> None:
        for callback in self.__eventListeners[event]:
            callback(self)
    
    def run(self) -> None:
        self.__occurEvent(EventType.INIT)
        self.__screen.onEnterScreen()

        while not self.__terminate:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__screen.onEscapeScreen()
                    self.__occurEvent(EventType.QUIT)
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__screen.onMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__screen.onMouseUp(event)
                elif event.type == pygame.MOUSEWHEEL:
                    self.__screen.onMouseWheel(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.__screen.onMouseMove(event)
                elif event.type == pygame.KEYDOWN:
                    self.__screen.onKeyDown(event)
                elif event.type == pygame.KEYUP:
                    self.__screen.onKeyUp(event)

            # Drawing
            self.__screen.draw()
            pygame.display.update()
            
            # Framerate
            if not self.__framerate == 0:
                self.__clock.tick(self.__framerate)
                
        pygame.quit()

    def setTitle(self, title: str) -> None:
        pygame.display.set_caption(title)

    def setWindowMode(self, width: int, height: int, displayMode: DisplayMode = DisplayMode.WINDOWED, resizable: Boolean = False, vsync: Boolean = False) -> None:
        flags = 0
        vs = 0

        if displayMode == DisplayMode.FULLSCREEN:
            flags |= pygame.FULLSCREEN
        elif displayMode == DisplayMode.NOFRAME:
            flags |= pygame.NOFRAME
        elif displayMode == DisplayMode.HIDDEN:
            flags |= pygame.HIDDEN

        if resizable:
            flags |= pygame.RESIZABLE

        if vsync:
            vs = 1

        pygame.display.set_mode((width, height), flags, vsync=vs)

    def toggleFullscreen(self) -> None:
        pygame.display.toggle_fullscreen()

    def setFramerate(self, framerate: int) -> None:
        self.__framerate = framerate

    def getCurrentFramerate(self) -> float:
        return self.__clock.get_fps()

    def setScreen(self, screen: Screen) -> None:
        self.__screen.onEscapeScreen()
        self.__screen = screen
        self.__screen.onEnterScreen()

    
    def terminate(self) -> None:
        self.__terminate = True

    def addEventListener(self, event: EventType, callback: Callable[[App], None]) -> None:
        if not event in self.__eventListeners:
            self.__eventListeners[event] = []
        self.__eventListeners[event].append(callback)

    def removeEventListener(self, event: EventType, callback: Callable[[App], None]) -> None:
        if event in self.__eventListeners:
            self.__eventListeners[event].remove(callback)

    def clearEventListeners(self, event: EventType) -> None:
        if event in self.__eventListeners:
            self.__eventListeners[event].clear()