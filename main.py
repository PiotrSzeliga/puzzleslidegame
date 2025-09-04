import pygame
import sys
from game import Game
from menu import Menu, MainMenu
from victoryscreen import VictoryScreen

g = Game()

while g.running:
    g.main_menu.menuloop()
    g.difficulty_menu.menuloop()
    g.gameloop()
    g.victory_screen.victory_loop()
    g.clock.tick(60)

pygame.display.quit()
pygame.quit()
sys.exit()