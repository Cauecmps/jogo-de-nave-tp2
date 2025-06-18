import pygame
import random
from .inimigo import Inimigo
# herda de inimigo
class InimigoRapido(Inimigo):
    def __init__(self):
        super().__init__() # Chama o __init__ da classe Inimigo
        self.velocidade = random.randint(4, 8) # Velocidade RÁPIDA
        self.image.fill((255, 0, 0)) # Cor vermelha para diferenciar

    def update(self):
        # A lógica de movimento é a mesma, mas usa a 'self.velocidade' que é mais alta
        self.rect.y += self.velocidade
        
        # Se o inimigo sair da tela, ele volta para o topo
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 760)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = random.randint(4, 8)