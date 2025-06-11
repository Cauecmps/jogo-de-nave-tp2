import pygame

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))  # Cor do projetil
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = -10  # O projetil vai para cima

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()  # Destruir o projetil quando sair da tela
