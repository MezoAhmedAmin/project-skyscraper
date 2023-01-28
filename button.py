
#* Imports
import pygame

#* Button Class
class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def getCoords(self):
    return self.rect.topleft

  def draw(self, surface, clicked, clieckedLast, sound = None, coords = None):
    if coords:
      self.rect.topleft = coords
    action = False
    #* Get mouse position
    pos = pygame.mouse.get_pos()

    #* Check mouseover and clicked conditions
    if self.rect.collidepoint(pos) and clicked and not clieckedLast:
      action = True
      if sound:
        sound.play()

    #* Draw button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action