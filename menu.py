
#* Imports and Initializations
import pygame
from math import sin
from pickle import dump

#* Menu Class
class Menu():
  #* Initializations
  def __init__(self, game):
    self.game = game
    self.runDisplay = True

  #* Blitting to the Screen
  def blitScreen(self):
    self.game.window.blit(self.game.display, (0, 0))
    pygame.display.update()

#* Main Menu Class
class MainMenu(Menu):
  #* Initializations
  def __init__(self, game):
    Menu.__init__(self, game)
    self.i = 0

  #* Displaying the Main Menu
  def displayMenu(self):
    self.runDisplay = True
    while self.runDisplay:
      self.game.checkEvents()
      self.game.display.blit(self.game.bcMain, (0, 0))

      if self.game.startBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.game.settings[1] == 1 else None):
        self.game.initVals()
        self.game.playing = True
        self.runDisplay = False
      if self.game.exitBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.game.settings[1] == 1 else None):
        self.game.running, self.game.playing = False, False
        self.runDisplay = False
      if self.game.settingsBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.game.settings[1] == 1 else None):
        self.game.currentMenu = SettingsMenu(self.game, self.game.settings)
        self.runDisplay = False

      pygame.display.set_caption("Skyscraper - Main Menu")

      if self.game.settings[2] == 2:
        self.i += 0.01
      elif self.game.settings[2] == 1:
        self.i += 0.005
      self.game.drawText("Project:", 40, self.game.fontB, 345, (self.game.sheight / 2) - 175 - (sin(self.i) * 18), self.game.black)
      self.game.drawText("Skyscraper", 100, self.game.fontB, self.game.swidth / 2, (self.game.sheight / 2) - 110 - (sin(self.i) * 18), self.game.black)

      self.blitScreen()
      self.game.resetKeys()

#* Pause Menu Class
class PauseMenu(Menu):
  #* Initializations
  def __init__(self, game):
    Menu.__init__(self, game)
    self.i = 0

  #* Displaying the Pause Menu
  def displayMenu(self):
    self.runDisplay = True
    if self.game.settings[1] == 1:
      self.game.buttonFX.play()
    while self.runDisplay:
      self.game.checkEvents()
      self.game.display.blit(self.game.overlay, (0, 0))
      self.game.drawHud()
      #* Resume
      if self.game.escKey:
        self.runDisplay = False
        self.game.playing = True
        self.game.currentMenu = MainMenu(self.game)
        if self.game.settings[1] == 1:
          self.game.buttonFX.play()

      #* Resume Button
      if self.game.resumeBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.game.settings[1] == 1 else None):
        self.runDisplay = False
        self.game.playing = True
        self.game.currentMenu = MainMenu(self.game)

      #* Exit Button
      if self.game.backBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.game.settings[1] == 1 else None, ((self.game.swidth * (2/3)) - (self.game.btnImg.get_width() / 2), (self.game.sheight / 2 + 20))):
        self.runDisplay = False
        self.game.playing = False
        self.game.currentMenu = MainMenu(self.game)
        self.game.hs = self.game.score if self.game.score > self.game.hs else self.game.hs
        with open("./Data/highscore.txt", "wb") as f:
          dump(self.game.hs, f)

      pygame.display.set_caption("Skyscraper - Game Paused")

      if self.game.settings[2] == 2:
        self.i += 0.02
      elif self.game.settings[2] == 1:
        self.i += 0.01
      self.game.drawText("Game Paused", 90, self.game.fontB, self.game.swidth / 2, (self.game.sheight / 2) - 70 - (sin(self.i) * 8), self.game.black)

      self.blitScreen()
      self.game.resetKeys()

#* Settings Menu Class
class SettingsMenu(Menu):
  def __init__(self, game, values):
    #* Initializations
    Menu.__init__(self, game)
    self.i = 0
    self.settings = [
      {
        "name": "HUD Position",
        "value": values[0],
        "values": ["TOP", "BOTTOM"]
      },
      {
        "name": "Sounds",
        "value": values[1],
        "values": ["OFF", "ON"]
      },
      {
        "name": "Text Animation",
        "value": values[2],
        "values": ["OFF", "LOW", "NORMAL"]
      }
    ]

  def displayMenu(self):
    self.runDisplay = True
    while self.runDisplay:
      self.game.checkEvents()
      self.game.display.blit(self.game.bcMain, (0, 0))

      pygame.display.set_caption("Skyscraper - Settings")

      sI = 0
      for setting in self.settings:
        sI += 1
        rect = pygame.Rect(60, (sI * 101) + 70, 984, 96)
        self.game.display.blit(self.game.setting, rect)
        self.game.drawText(f"{setting['name']}: {setting['values'][setting['value']]}", 35, self.game.font, rect.centerx, rect.y + 40, self.game.black)

        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos) and self.game.clicked and not self.game.clickedLast:
          setting["value"] += 1
          if len(setting["values"]) <= setting["value"]:
            setting["value"] = 0
          if self.settings[1]["value"] == 1:
            self.game.buttonFX.play()

      if self.settings[2]["value"] == 2:
        self.i += 0.02
      elif self.settings[2]["value"] == 1:
        self.i += 0.01
      self.game.drawText("Settings", 90, self.game.fontB, self.game.swidth / 2, 100 - (sin(self.i) * 7), self.game.black)

      if self.game.backBtn.draw(self.game.display, self.game.clicked, self.game.clickedLast, self.game.buttonFX if self.settings[1]["value"] == 1 else None, ((self.game.swidth / 2) - (self.game.btnImg.get_width() / 2), self.game.sheight - 100)):
        self.game.settings = []
        for setting in self.settings:
          self.game.settings.append(setting["value"])
        with open("./Data/settings.txt", "wb") as f:
          dump(self.game.settings, f)
        self.game.currentMenu = MainMenu(self.game)
        self.runDisplay = False

      self.blitScreen()
      self.game.resetKeys()