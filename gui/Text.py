import pygame

from utils import rectOffset

class Text():
  def __init__(self, text, center):
    self.text = text
    self.center = center
    self.font = pygame.font.Font("fonts/courier-bold.ttf", 14)

  def blit(self, screen):
    textSurface = self.font.render(self.text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.center = self.center
    offSurface = self.font.render(self.text, True, (255, 255, 255))
    offTextRect = rectOffset(textRect, 1)
    screen.blit(offSurface, offTextRect)
    screen.blit(textSurface, textRect)
