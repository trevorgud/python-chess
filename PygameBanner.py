import pygame

from utils import rectOffset

class PygameBanner():
  def __init__(self, text, topPad = 0, color = (0, 0, 0)):
    self.text = text
    self.topPad = topPad
    self.color = color
    self.font = pygame.font.Font("fonts/bitstream.ttf", 12)

  def blit(self, screen):
    lines = self.text.split("\n")
    lineNum = 0
    for line in lines:
      lineSurface = self.font.render(line, True, self.color)
      offSurface = self.font.render(line, True, (255, 255, 255))
      lineRect = lineSurface.get_rect()
      lineRect.center = screen.get_rect().center
      lineRect.top = (lineRect.height + 1) * lineNum
      offRect = rectOffset(lineRect, 1)
      screen.blit(offSurface, offRect)
      screen.blit(lineSurface, lineRect)
      lineNum += 1
