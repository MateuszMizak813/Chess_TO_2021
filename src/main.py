import pygame
from chess_board import ChessBoard
import constants as con


"""
Główna klasa odpowiedzialna za uruchominie i zarządzanie oknem gry, eventami oraz przygotowująco wszystkie niezbędne elementy
"""
class main():
    """
    Kontruktor klasy głównej, tworzy instancje okna gry, szchownicy i innych niezbędnych rzeczy oraz zawiera główną pętle programu
    """
    def __init__(self) -> None:
        # Inicjalizacja biblioteki pygame
        pygame.init()
        self.__vsAI = self.chooseGamemode()

        # Ustawienia ekranu i zainicjowanie niezbędnych elementów
        self.__chess_window = pygame.display.set_mode((640,640))
        self.__chess_window.fill((255,255,255))
        self.__clock = pygame.time.Clock()
        self.__chess_board = ChessBoard(self.__chess_window, againstAi=self.__vsAI)

        # Wejście do pętli głównej
        self.mainLoop()


    """
    Główna pętla programu odpowiedzialna za przechwytywanie eventów
    """
    def mainLoop(self):
        # Ustawienie warunku zakończenia pętli
        self.__loop = True

        # Główna pętla programu 
        while self.__loop:

            # Przechwytywanie wydarzeń na ekranie
            for event in pygame.event.get():

                # Nacisnięcie X - wyłączenie programu
                if event.type == pygame.QUIT:
                    self.__loop = False

                # Naciśnięcie przycisku myszy
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    position = pygame.mouse.get_pos()

                    # Przycisk myszy naciśnięty w obrębie szachownicy
                    if position[0] <= con.field_size * 8 and position[1] <= con.field_size *8:
                        column = position[0] // con.field_size
                        row = position[1] // con.field_size
                        self.__chess_board.leftClickOnChessBoard(row,column)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.__chess_board.undo()
                        if self.__vsAI:
                            self.__chess_board.undo()
                    if event.key == pygame.K_RIGHT:
                        self.__chess_board.forward()
                        if self.__vsAI:
                            self.__chess_board.forward()
        
            # Odświeżanie obrazu
            self.__clock.tick(15)
            pygame.display.flip()

    def chooseGamemode(self):
        window = pygame.display.set_mode((320,160))
        window.fill("white")
        clock = pygame.time.Clock()
        loop = True
        for i in [0,79,158]:
            pygame.draw.line(window, "black", (0,i),(320,i),2)
        for i in [0,318]:
            pygame.draw.line(window, "black", (i,0),(i,160),2)
        myfont = pygame.font.SysFont("monospace", 30)
        label1 = myfont.render("vs Player", 1, "black")
        label2 = myfont.render("vs AI", 1, "black")
        window.blit(label1,(80,25))
        window.blit(label2,(110,105))
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    position = pygame.mouse.get_pos()

                    # Przycisk myszy naciśnięty w obrębie szachownicy
                    if position[1] <= 79:
                        vsAI = False
                        loop = False
                    elif position[1] >= 80:
                        loop = False
                        vsAI = True
                        




            clock.tick(15)
            pygame.display.flip()
        pygame.quit()
        return vsAI


    
# Uruchomienie Programu
if __name__ == "__main__":
    main()