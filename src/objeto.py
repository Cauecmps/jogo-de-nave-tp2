import pygame
import random

class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Cor do inimigo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 760)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(2, 5)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 760)
            self.rect.y = random.randint(-100, -40)
