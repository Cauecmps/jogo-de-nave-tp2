import pygame
import random

# herda de inimigo
class InimigoLento:
    def __init__(self):
        super().__init__()  # Chama o __init__ da classe Inimigo para configurar o básico
        self.velocidade = random.randint(1, 3)  # Velocidade LENTA
        self.image.fill((0, 0, 255))  # Cor azul para diferenciar

    def update(self):
        # Implementação do comportamento específico deste inimigo
        self.rect.y += self.velocidade

        # Se o inimigo sair da tela, ele volta para o topo em uma nova posição
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 760)
            self.rect.y = random.randint(-100, -40)
            # A velocidade também pode ser re-sorteada se desejar
            self.velocidade = random.randint(1, 3)