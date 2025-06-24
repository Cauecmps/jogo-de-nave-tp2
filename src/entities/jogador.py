import pygame
import os

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        caminho_imagem = os.path.join('assets', 'images', 'jogador.png')
        try:
            self.image = pygame.image.load(caminho_imagem).convert_alpha()
        except pygame.error:
            print(f"ERRO: Imagem do jogador nao encontrada em '{caminho_imagem}'")
            # cria uma superficie, caso a imagem nao carregue
            self.image = pygame.Surface((50, 40))
            self.image.fill((0, 255, 0)) # Verde

        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)
        self.velocidade = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.velocidade