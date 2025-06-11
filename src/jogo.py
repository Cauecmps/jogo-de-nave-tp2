import pygame
import sys
from nave import Nave
from projetil import Projetil
from objeto import Objeto

# Inicializar o Pygame
pygame.init()

# Configuração da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo de Nave")

# Grupo de sprites
all_sprites = pygame.sprite.Group()
projetis = pygame.sprite.Group()
objetos = pygame.sprite.Group()

# Criando instâncias
nave = Nave()
all_sprites.add(nave)

# Função para verificar colisões
def verificar_colisoes():
    global pontuacao
    colisao = pygame.sprite.groupcollide(projetis, objetos, True, True)
    for _ in colisao:
        pontuacao += 1

# Função para disparar
def disparar():
    projetil = Projetil(nave.rect.centerx, nave.rect.top)
    all_sprites.add(projetil)
    projetis.add(projetil)

# Criar inimigos
def criar_inimigos():
    inimigo = Objeto()
    all_sprites.add(inimigo)
    objetos.add(inimigo)

# Loop principal do jogo
pontuacao = 0
clock = pygame.time.Clock()

# Criar inimigos a cada 2 segundos
pygame.time.set_timer(pygame.USEREVENT, 2000)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                disparar()  # Disparar quando pressionar a barra de espaço
        elif evento.type == pygame.USEREVENT:
            criar_inimigos()  # Criar inimigos a cada 2 segundos

    # Atualizar o estado dos sprites
    all_sprites.update()
    verificar_colisoes()

    # Preencher a tela
    tela.fill((0, 0, 0))

    # Desenhar todos os sprites
    all_sprites.draw(tela)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar os FPS
    clock.tick(60)
