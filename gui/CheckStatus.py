import pygame

from Color import Color

class CheckStatus():
  def __init__(self, isCheck, isCheckmate, rect):
    self.isCheck = isCheck
    self.isCheckmate = isCheckmate
    self.rect = rect
    self.font = pygame.font.Font("fonts/courier-bold.ttf", 16)

  def blit(self, screen):
    text = ""
    if self.isCheck:
      text = "Check"
    if self.isCheckmate:
      text = "Checkmate"

    textSurface = self.font.render(text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.left = self.rect.left
    textRect.top = self.rect.top

    if self.isCheck or self.isCheckmate:
      screen.blit(textSurface, textRect)