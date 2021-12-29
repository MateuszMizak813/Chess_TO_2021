import pygame
import constants as con


"""
Klasa odpowiedzialna za przechowywanie stanu gry w celu umożliwienia zapisu i odczytu wybranych tur 
NOT IMPLEMENTED YET
"""
class GameState():
    def __init__(self, board, turn = 1) -> None:
        self.__board = board
        self.__turn = turn
    def getBoard(self):
        return self.__board
    def getTurn(self):
        return self.__turn