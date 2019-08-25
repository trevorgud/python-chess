import pygame

from utils import rectOffset

class TextInput():
  def __init__(self, rect, maxLen):
    self.text = ""
    self.active = False
    self.rect = rect
    self.maxLen = maxLen
    self.font = pygame.font.Font("fonts/courier-bold.ttf", 14)

  def blit(self, screen):
    borderRect = pygame.Rect((0, 0), (self.rect.width + 2, self.rect.height + 2))
    borderRect.center = self.rect.center
    offRect = rectOffset(borderRect, 1)
    borderWidth = 2 if self.active else 1
    pygame.draw.rect(screen, (255, 255, 255), offRect, borderWidth)
    pygame.draw.rect(screen, (0, 0, 0), borderRect, borderWidth)
    text = self.text
    if(self.active):
      text += "|"
    textSurface = self.font.render(text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.center = self.rect.center
    offSurface = self.font.render(text, True, (255, 255, 255))
    offTextRect = rectOffset(textRect, 1)
    screen.blit(offSurface, offTextRect)
    screen.blit(textSurface, textRect)

  def handle(self, event, pos):
    if self.active and event.type == pygame.KEYDOWN:
      if event.key == pygame.K_BACKSPACE:
        self.text = self.text[:-1]
      elif event.unicode.isprintable() and len(self.text) < self.maxLen:
        self.text += event.unicode
    if event.type == pygame.MOUSEBUTTONUP:
      self.active = self.rect.collidepoint(pos)
