from game import Game
from menu import Menu, MainMenu

g = Game()

while g.running:
    g.menu.menuloop()
    g.gameloop()
