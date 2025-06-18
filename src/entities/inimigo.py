# classe abstrata
from abc import ABC, abstractmethod
import pygame
import random

class Inimigo(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        # Configurações visuais e de posição que são comuns a todos os inimigos
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 760)  # Posição inicial aleatória no eixo X
        self.rect.y = random.randint(-100, -40) # Aparece fora da tela, no topo

    @abstractmethod
    def update(self):
        pass
    
    