
#* Imports and Initializations
from game import Game
g = Game()

#* Run Loop
while g.running:
  g.currentMenu.displayMenu()
  g.gameLoop()