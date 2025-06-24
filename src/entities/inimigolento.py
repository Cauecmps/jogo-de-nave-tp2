import pygame
import random
from .inimigo import Inimigo # Importa a classe Inimigo do mesmo diretório

class InimigoLento(Inimigo):

    def __init__(self):
        super().__init__()
        
        self.velocidade = random.randint(1, 3)
        self.image.fill((0, 0, 255)) # Agora o self.image já foi criado pela classe pai

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 760)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = random.randint(1, 3)