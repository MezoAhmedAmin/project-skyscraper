
#* Imports and Initializations
import pygame
pygame.init()
from menu import MainMenu, PauseMenu
from button import Button
import gameClasses as gclasses
from random import randint
from pickle import dump, load
from math import tan

class Game():
  def __init__(self):
    #* Initializations
    pygame.init()
    self.running, self.playing = True, False
    self.swidth, self.sheight = 1104, 720
    self.display = pygame.Surface((self.swidth, self.sheight))
    self.window = pygame.display.set_mode((self.swidth, self.sheight))
    pygame.display.set_icon(pygame.image.load("./Assets/Images/icon.ico"))
    self.currentMenu = MainMenu(self)
    self.clicked, self.clickedLast = False, False
    self.clock = pygame.time.Clock()
    self.maxPlats = 12
    self.maxWalls = 6
    self.colorList = ["LBlue", "Blue", "Purple", "Pink", "Red", "Brown", "Orange", "Yellow", "LGreen", "Green"]

    #* Settings
    self.settings = []
    with open("./Data/settings.txt", "rb") as f:
      self.settings = load(f)

    #* Highscore
    self.score = 0
    self.hs = 0
    with open("./Data/highscore.txt", "rb") as f:
      self.hs = load(f)

    #* Fonts
    self.font = "./Assets/Fonts/ComicCodeLigatures-Regular.otf"
    self.fontSB = "./Assets/Fonts/ComicCodeLigatures-SemiBold.otf"
    self.fontB = "./Assets/Fonts/ComicCodeLigatures-Bold.otf"

    #* Images
    self.bcMain = pygame.image.load("./Assets/Images/bc-main.png")
    self.bcSky = pygame.image.load("./Assets/Images/bc-sky.png")
    self.hud = pygame.image.load("./Assets/Images/hud.png")
    self.overlay = pygame.image.load("./Assets/Images/overlay.png")
    self.fadeTrans = pygame.image.load("./Assets/Images/fadeTrans.png")
    self.setting = pygame.image.load("./Assets/Images/setting.png")

    #* Buttons
    self.startBtnImg = pygame.image.load("Assets/Images/Buttons/start.png")
    self.startBtn = Button((self.swidth / 4) - (self.startBtnImg.get_width() / 2), self.sheight / 2 + 20, self.startBtnImg)
    self.exitBtnImg = pygame.image.load("Assets/Images/Buttons/exit.png")
    self.exitBtn = Button((self.swidth * .75) - (self.exitBtnImg.get_width() / 2), self.sheight / 2 + 20, self.exitBtnImg)
    self.resumeBtnImg = pygame.image.load("./Assets/Images/Buttons/resume.png")
    self.resumeBtn = Button((self.swidth / 3) - (self.resumeBtnImg.get_width() / 2), (self.sheight / 2 + 20), self.resumeBtnImg)
    self.backBtnImg = pygame.image.load("./Assets/Images/Buttons/back.png")
    self.backBtn = Button((self.swidth * (2/3)) - (self.backBtnImg.get_width() / 2), (self.sheight / 2 + 20), self.backBtnImg)
    self.retryBtnImg = pygame.image.load("./Assets/Images/Buttons/retry.png")
    self.retryBtn = Button((self.swidth / 3) - (self.resumeBtnImg.get_width() / 2), (self.sheight / 2 + 20), self.retryBtnImg)
    self.settingsBtnImg = pygame.image.load("./Assets/Images/Buttons/settings.png")
    self.settingsBtn = Button((self.swidth / 2) - (self.resumeBtnImg.get_width() / 2), (self.sheight / 2 + 20), self.settingsBtnImg)

    #* Colors
    self.black = (0, 0, 0)
    self.white = (255, 255, 255)

    #* Keys
    self.escKey = False
    self.wKey = False
    self.aKey = False
    self.dKey = False
    self.spaceKey = False

    #* Sounds
    self.jumpFX = pygame.mixer.Sound("./Assets/Sounds/jump.wav")
    self.jumpFX.set_volume(0.3)
    self.buttonFX = pygame.mixer.Sound("./Assets/Sounds/button.wav")
    self.buttonFX.set_volume(0.6)
    self.walkFX = pygame.mixer.Sound("./Assets/Sounds/walk.wav")
    self.walkFX.set_volume(0.5)
    self.deathFX = pygame.mixer.Sound("./Assets/Sounds/death.wav")
    self.slideFX = pygame.mixer.Sound("./Assets/Sounds/slide.wav")

    #* Classes
    self.player = gclasses.Player(100, self.sheight - 160, self)
    self.platGroup = pygame.sprite.Group()
    self.boundGroup = pygame.sprite.Group()
    self.wallGroup = pygame.sprite.Group()
    self.bgGroup = pygame.sprite.Group()

  #* Game Loop
  def gameLoop(self):
    while self.playing:
      self.clock.tick(60)
      self.checkEvents()

      if not self.gameOver:
        if self.player.rect.top > self.sheight:
          self.gameOver = True
          if self.settings[1] == 1:
            self.deathFX.play()

        if self.escKey:
          self.playing = False
          self.currentMenu = PauseMenu(self)
        self.display.blit(self.bcSky, (0, 0))

        pygame.display.set_caption("Skyscraper - Game")

        self.scroll = self.player.update()

        if len(self.platGroup) < self.maxPlats:
          platWidth = randint(100, 140)
          platX = randint(250, self.swidth - platWidth - 250)
          platY = self.platform.rect.y - randint(80, 125)
          platType = randint(0, 1)
          self.platform = gclasses.Platform(platX, platY, platWidth, platType, self)
          self.platGroup.add(self.platform)

        if len(self.wallGroup) < self.maxWalls:
          wallX = self.swidth - 144 if self.wall.rect.x == 96 else 96
          wallY = self.wall.rect.y - 768
          bgY = 0
          wallColor = self.wall.colorUr + 0.5 if self.wall.colorUr + 1 < len(self.colorList) else 0
          self.wall = gclasses.Wall(wallX, wallY, wallColor, self.colorList, self)
          self.wallGroup.add(self.wall)
          bg = gclasses.Background(wallX + 48, wallY, wallColor, self.colorList, self)
          self.bgGroup.add(bg)
          wallX = self.swidth - 144 if self.wall.rect.x == 96 else 96
          self.wall = gclasses.Wall(wallX, wallY, wallColor, self.colorList, self)
          self.wallGroup.add(self.wall)

        self.bgGroup.update(self.scroll)
        self.platGroup.update(self.scroll)
        self.boundGroup.update(self.scroll)
        self.wallGroup.update(self.scroll)

        if self.scroll > 0:
          self.score += round(round(self.scroll) / 4)

        self.bgGroup.draw(self.display)
        self.player.draw()
        self.platGroup.draw(self.display)
        self.boundGroup.draw(self.display)
        self.wallGroup.draw(self.display)

        self.drawHud()

      else:
        self.fade += 1
        if self.fade < 60:
          self.display.blit(self.fadeTrans, (0, 0))
        if (self.fade == 70 or self.fade == 90 or self.fade == 100) and self.settings[1] == 1:
          self.slideFX.play()
        if self.fade > 70:
          self.display.fill(self.black)
          self.drawText("Game Over", 90, self.fontB, self.swidth / 2, self.sheight / 2 - 100 + (tan(self.i) * 4.5), self.white)
          self.hs = self.score if self.score > self.hs else self.hs
          with open("./Data/highscore.txt", "wb") as f:
            dump(self.hs, f)
          self.drawText(f"Score: {self.score}   Highscore: {self.hs}", 30, self.fontSB, self.swidth / 2, self.sheight / 2 - 40 + (tan(self.i) * 4.5), self.white)
          if self.i < 81:
            self.i += 0.0025
          if self.fade > 90:
            if self.retryBtn.draw(self.display, self.clicked, self.clickedLast, self.buttonFX if self.settings[1] == 1 else None, ((self.swidth / 3) - (self.resumeBtnImg.get_width() / 2), (self.sheight / 2 + 15) - tan(self.i - 0.05) * 4.5)):
              self.initVals()
              self.playing = True
          if self.fade > 100:
            if self.backBtn.draw(self.display, self.clicked, self.clickedLast, self.buttonFX if self.settings[1] == 1 else None, ((self.swidth * (2/3)) - (self.backBtnImg.get_width() / 2), (self.sheight / 2 + 15) - tan(self.i - 0.075) * 4.5)):
              self.playing = False
              self.currentMenu = MainMenu(self)

      #* Blitting to the Screen
      self.window.blit(self.display, (0, 0))
      pygame.display.update()
      self.resetKeys()

  #* Initializing the Game Values
  def initVals(self):
    #* Boundary Initialization
    self.boundGroup.empty()
    boundData = [
      ["floor", 0, self.sheight - 96],
      ["door", 96, self.sheight - 192],
      ["dwall", self.swidth - 144, self.sheight - 192],
    ]

    for b in boundData:
      bound = gclasses.Bound(b[0], b[1], b[2])
      self.boundGroup.add(bound)

    #* Other Initializations
    self.player.rect.x, self.player.rect.y = 150, self.sheight - 100
    self.player.yVel, self.player.dir = 0, 1
    self.platform = gclasses.Platform(0, self.sheight - 110, 3, 0, self)
    self.platGroup.empty()
    self.wall = gclasses.Wall(self.swidth - 144, self.sheight - 192, -0.5, self.colorList, self)
    self.wallGroup.empty()
    self.bgGroup.empty()
    self.bgGroup.add(gclasses.Background(144, self.sheight - 192, 0, self.colorList, self))
    self.score = 0
    self.gameOver = False
    self.fade = 0
    self.i = 80.115

  #* Events
  def checkEvents(self):
    for event in pygame.event.get():
      #* Quit Event
      if event.type == pygame.QUIT:
        self.running, self.playing = False, False
        self.currentMenu.runDisplay = False
      #* Key Presses
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.escKey = True
        if event.key == pygame.K_w:
          self.wKey = True
        if event.key == pygame.K_a:
          self.aKey = True
        if event.key == pygame.K_d:
          self.dKey = True
        if event.key == pygame.K_SPACE:
          self.spaceKey = True

      #* Key Releases
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          self.wKey = False
        if event.key == pygame.K_a:
          self.aKey = False
        if event.key == pygame.K_d:
          self.dKey = False
        if event.key == pygame.K_SPACE:
          self.spaceKey = False

    self.clickedLast = self.clicked

    if pygame.mouse.get_pressed()[0] == 1:
      self.clicked = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

  #* Reseting the Keys
  def resetKeys(self):
    self.escKey = False

  #* Drawing Text
  def drawText(self, text, size, font, x, y, color, center: bool = True):
    font = pygame.font.Font(font, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    if center == True:
      textRect.center = (x, y)
    else:
      textRect.x, textRect.y = x, y
    self.display.blit(textSurface, textRect)

  #* Drawing the HUD
  def drawHud(self):
    if self.settings[0] == 1:
      self.display.blit(self.hud, (0, self.sheight - self.hud.get_height()))
      self.drawText(f"FPS: {str(int(self.clock.get_fps()))}", 25, self.fontSB, 10, self.sheight - 40, self.black, False)
      self.drawText(f"SCORE: {self.score}     HIGH SCORE: {self.hs}", 25, self.fontSB, 200, self.sheight - 40, self.black, False)
    else:
      self.display.blit(self.hud, (0, 0))
      self.drawText(f"FPS: {str(int(self.clock.get_fps()))}", 25, self.fontSB, 10, 0, self.black, False)
      self.drawText(f"SCORE: {self.score}     HIGH SCORE: {self.hs}", 25, self.fontSB, 200, 0, self.black, False)