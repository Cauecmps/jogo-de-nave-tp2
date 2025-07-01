import pygame
import random
import os
from .inimigo import Inimigo # Importa a classe Inimigo do mesmo diretório

class InimigoLento(Inimigo):

    def __init__(self):
        super().__init__()
        caminho_imagem = os.path.join('assets', 'images', 'inimigo_lento.png')
        try:
            self.image = pygame.image.load(caminho_imagem).convert_alpha()
        except pygame.error:
            print(f"ERRO: Imagem do inimigo lento não encontrada em '{caminho_imagem}'")
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 0, 255)) # Azul
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 760)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(1, 3)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 760)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = random.randint(1, 3)