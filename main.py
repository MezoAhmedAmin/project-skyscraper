"""
* Idea: THE TOWER
* A randomly generated tower that you have to climb
* You get points for how far you progress on the tower
? Obstacles that will make you lose progress or make you start from the beginning
? RISING LAVA
? Powerups
? Maybe a few enemies

* Slime / Magic / Toppat-ish theme
* BTD5 NINJA
"""

#* Imports and Initializations
from game import Game
g = Game()

#* Run Loop
while g.running:
  g.currentMenu.displayMenu()
  g.gameLoop()