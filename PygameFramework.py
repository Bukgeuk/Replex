from __future__ import annotations

import sys
from enum import Enum
from typing import Callable, Dict, List, Optional

import pygame

import api.font
import api.key
import api.mouse
from components.Audio import Audio
from components.Base import Positioning
from components.Image import Image
from components.Screen import Screen


class EventType(Enum):
    RUN = 0
    QUIT = 1

class DisplayMode(Enum):
    WINDOWED = 0
    FULLSCREEN = 1
    NOFRAME = 2
    HIDDEN = 3

class App:
    def __init__(self) -> None:
        pygame.init()

        self.__terminate = False
        self.__clock = pygame.time.Clock()
        self.__framerate: int = 0
        self.__eventListeners: Dict[EventType, List[Callable[[App], None]]] = {}
        self.__screen: Optional[Screen]
        self.__pygameSurface: Optional[pygame.surface.Surface] = None

    def __occurEvent(self, event: EventType) -> None:
        if event in self.__eventListeners:
            for callback in self.__eventListeners[event]:
                callback(self)
    
    def run(self, initialScreen: Screen) -> None:
        self.__screen = initialScreen

        self.__occurEvent(EventType.RUN)
        self.__screen.onEnterScreen()

        while not self.__terminate:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__screen.onEscapeScreen()
                    self.__occurEvent(EventType.QUIT)
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not (event.button == 4 or event.button == 5):
                        self.__screen.onMouseDown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not (event.button == 4 or event.button == 5):
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
            self.__screen._tick()
            self.__screen.draw()

            assert self.__pygameSurface is not None, 'Use setWindowMode before running'

            self.__pygameSurface.blit(self.__screen.getPygameSurface(), (0, 0))
            pygame.display.update()         
            
            # Framerate
            if not self.__framerate == 0:
                self.__clock.tick(self.__framerate)
                
        pygame.quit()
        sys.exit()

    def setTitle(self, title: str) -> None:
        pygame.display.set_caption(title)

    def setWindowMode(self, width: int, height: int, displayMode: DisplayMode = DisplayMode.WINDOWED, resizable: bool = False, vsync: bool = False) -> None:
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

        self.__pygameSurface = pygame.display.set_mode((width, height), flags, vsync=vs)

    def toggleFullscreen(self) -> None:
        pygame.display.toggle_fullscreen()

    def setFramerate(self, framerate: int) -> None:
        self.__framerate = framerate

    def getCurrentFramerate(self) -> float:
        return self.__clock.get_fps()

    def setScreen(self, screen: Screen) -> None:
        if self.__screen is not None:
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
