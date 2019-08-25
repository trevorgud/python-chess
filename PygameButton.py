import pygame

class PygameButton():
  def __init__(self, text, rect, handler, color = (128, 128, 128)):
    self.text = text
    self.rect = rect
    self.handler = handler
    self.color = color
    self.font = pygame.font.Font("fonts/courier-new.ttf", 14)

  def blit(self, screen):
    borderRect = pygame.Rect((0, 0), (self.rect.width + 2, self.rect.height + 2))
    borderRect.center = self.rect.center
    pygame.draw.rect(screen, (0, 0, 0), borderRect)
    pygame.draw.rect(screen, self.color, self.rect)
    textSurface = self.font.render(self.text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.center = self.rect.center
    screen.blit(textSurface, textRect)

  def handle(self, event, pos):
    if(event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pos)):
      self.handler()
