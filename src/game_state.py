import pygame
import constants as con


"""
Klasa odpowiedzialna za przechowywanie stanu gry w celu umożliwienia zapisu i odczytu wybranych tur 
NOT IMPLEMENTED YET
"""
class GameHistory():
    def __init__(self):
        self.__move_list = []

    def addMove(self, move):
        self.__move_list.append(move)
    
    def undoMove(self):
        if len(self.__move_list) > 0:
            return self.__move_list.pop(-1)