import pygame

from Color import Color

class TurnText():
  def __init__(self, turn, rect):
    self.turn = turn
    self.rect = rect
    self.font = pygame.font.Font("fonts/courier-bold.ttf", 16)

  def blit(self, screen):
    turnSurface = self.font.render("Turn: ", True, (0, 0, 0))
    turnRect = turnSurface.get_rect()
    turnRect.left = self.rect.left
    turnRect.top = self.rect.top

    turnRgb = (0, 0, 0) if self.turn == Color.BLACK else (255, 255, 255)
    colorSurface = self.font.render(self.turn.name, True, turnRgb)
    colorRect = colorSurface.get_rect()
    colorRect.left = turnRect.left + turnRect.width
    colorRect.top = self.rect.top

    screen.blit(turnSurface, turnRect)
    screen.blit(colorSurface, colorRect)
