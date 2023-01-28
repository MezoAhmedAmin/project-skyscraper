import pygame
from math import floor
from random import randint, choice

#* Platforms Class
class Platform(pygame.sprite.Sprite):
  def __init__(self, x, y, w, type, game):
    pygame.sprite.Sprite.__init__(self)
    platNormal = pygame.image.load("./Assets/Images/platNormal.png")
    platMoving = pygame.image.load("./Assets/Images/platMoving.png")
    self.game = game
    self.moving = True if type == 1 and self.game.score >= 450 else False
    self.moveC = randint(0, 50)
    self.direction = choice([-1, 1])
    self.speed = randint(1, 3) if self.game.score >= 1500 else randint(1, 2)
    self.max = randint(90, 130)
    self.image = platMoving if self.moving else platNormal
    self.image = pygame.transform.scale(self.image, (w, 24))
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = x, y

  def update(self, scroll):
    #* Moving the Platform
    if self.moving:
      self.moveC += 1
      self.rect.x += self.direction * self.speed

    if self.moveC >= self.max or self.rect.left <= 194 or self.rect.right >= self.game.swidth - 194:
      self.direction *= -1
      self.moveC = 0

    #* Update Platform Vetrtical Position
    self.rect.y += scroll

    #* Check if platform has gone over the screen
    if self.rect.y > self.game.sheight:
      self.kill()

#* Boundaries  Class
class Bound(pygame.sprite.Sprite):
  def __init__(self, type, x, y):
    pygame.sprite.Sprite.__init__(self)

    floor = pygame.image.load("./Assets/Images/floor.png")
    door = pygame.image.load("./Assets/Images/door.png")
    dwall = pygame.image.load("./Assets/Images/dwall.png")

    if type == "floor":
      self.image = floor
    if type == "door":
      self.image = door
    if type == "dwall":
      self.image = dwall

    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = x, y

  def update(self, scroll):
    #* Update Bound Vetrtical Position
    self.rect.y += scroll

#* Wall Class
class Wall(pygame.sprite.Sprite):
  def __init__(self, x, y, color, colorList, game):
    pygame.sprite.Sprite.__init__(self)
    self.colorUr = color
    self.color = floor(color)

    self.game = game
    self.image = pygame.image.load("./Assets/Images/Walls/wall" + colorList[self.color] + ".png")
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = x, y

  def update(self, scroll):
    #* Update Wall Vetrtical Position
    self.rect.y += scroll

    #* Check if platform has gone over the screen
    if self.rect.y > self.game.sheight:
      self.kill()

#* Background Class
class Background(pygame.sprite.Sprite):
  def __init__(self, x, y, color, colorList, game):
    pygame.sprite.Sprite.__init__(self)
    self.color = floor(color)

    self.game = game
    self.image = pygame.image.load("./Assets/Images/Backgrounds/bg" + colorList[self.color] + ".png")
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = x, y

  def update(self, scroll):
    #* Update Wall Vetrtical Position
    self.rect.y += scroll

    #* Check if platform has gone over the screen
    if self.rect.y > self.game.sheight:
      self.kill()

#* Player Class
class Player():
  def __init__(self, x, y, game):
    self.imgsR = []
    self.imgsL = []
    self.index, self.counter = 0, 0
    for num in range(1, 5):
      imgR = pygame.image.load(f"./Assets/Images/player{num}.png")
      imgR = pygame.transform.scale(imgR, (32, 36))
      self.imgsR.append(imgR)
      imgL = pygame.transform.flip(imgR, True, False)
      self.imgsL.append(imgL)
    self.img = self.imgsR[self.index]
    self.rect = self.img.get_rect()
    self.rect.x, self.rect.y = x, y
    self.width, self.height = self.img.get_width(), self.img.get_height()
    self.game = game
    self.yVel = 0
    self.jumped = False
    self.dir = 1
    self.sCounter = 0

  def update(self):
    dx = 0
    dy = 0
    wCool = 6
    sCool = 6
    self.sCounter += 1
    scroll = 0

    #* Get Key Presses
    if (self.game.wKey or self.game.spaceKey) and not self.jumped and self.yVel <= 0:
      self.yVel = -14
      self.jumped = True
      if self.game.settings[1] == 1:
        self.game.jumpFX.play()
    if self.game.aKey:
      dx -= 5
      self.dir = -1
      if self.sCounter > sCool and not self.jumped and self.yVel == 0:
        if self.game.settings[1] == 1:
          self.game.walkFX.play()
        self.sCounter = 0
    if self.game.dKey:
      dx += 5
      self.dir = 1
      if self.sCounter > sCool and not self.jumped and self.yVel == 0:
        if self.game.settings[1] == 1:
          self.game.walkFX.play()
        self.sCounter = 0

    if self.game.dKey or self.game.aKey:
      self.counter += 1
    if not self.game.dKey and not self.game.aKey:
      self.counter = 0
      self.index = 0
      if self.dir == 1:
        self.img = self.imgsR[self.index]
      else:
        self.img = self.imgsL[self.index]

    #* Animation
    if self.counter > wCool:
      self.counter = 0
      self.index += 1
      if self.index >= len(self.imgsR):
        self.index = 0
    if self.dir == 1:
      self.img = self.imgsR[self.index]
    else:
      self.img = self.imgsL[self.index]

    #* Gravity
    self.yVel += 0.5
    dy += self.yVel

    #* Check for Collision with Boundaries
    for bound in self.game.boundGroup:
      #* Check for collision in the x axis
      if bound.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        dx = 0

      #* Check for collision in the y axis
      if bound.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
        #* Check if below the ground (Jumping)
        if self.yVel < 0:
          dy = bound.rect.bottom - self.rect.top
          self.yVel = 0
        #* Check if above the ground (Falling)
        elif self.yVel >= 0:
          dy = bound.rect.top - self.rect.bottom
          self.yVel = 0
          self.jumped = False

    #* Check for Collision with Walls
    for wall in self.game.wallGroup:
      #* Check for collision in the x axis
      if wall.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        dx = 0

    #* Check for Collision with Platforms
    for plat in self.game.platGroup:
      if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
        #* Check if above the ground (Falling)
        if self.yVel >= 0 and self.rect.bottom < plat.rect.centery:
          dy = plat.rect.top - self.rect.bottom
          self.yVel = 0
          self.jumped = False

    #* Update Scroll
    if self.rect.top <= self.game.sheight / 4:
      if self.yVel < 0:
        scroll = -dy

    #* Update Player Coords
    self.rect.x += dx
    self.rect.y += dy + scroll

    return scroll

  #* Draw Player onto Screen
  def draw(self):
    self.game.display.blit(self.img, self.rect)