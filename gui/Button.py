import pygame

from utils import rectOffset

class Button():
  def __init__(self, text, rect, handler, color = (128, 128, 128)):
    self.text = text
    self.rect = rect
    self.handler = handler
    self.color = color
    self.font = pygame.font.Font("fonts/courier-bold.ttf", 14)

  def blit(self, screen):
    borderRect = pygame.Rect((0, 0), (self.rect.width + 2, self.rect.height + 2))
    borderRect.center = self.rect.center
    offRect = rectOffset(borderRect, 1)
    pygame.draw.rect(screen, (255, 255, 255), offRect, 1)
    if self.color is not None:
      pygame.draw.rect(screen, (0, 0, 0), borderRect)
      pygame.draw.rect(screen, self.color, self.rect)
    else:
      pygame.draw.rect(screen, (0, 0, 0), borderRect, 1)
    textSurface = self.font.render(self.text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.center = self.rect.center
    offSurface = self.font.render(self.text, True, (255, 255, 255))
    offTextRect = rectOffset(textRect, 1)
    screen.blit(offSurface, offTextRect)
    screen.blit(textSurface, textRect)

  def handle(self, event, pos):
    if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pos):
      self.handler()
