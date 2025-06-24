# TP2_POO/main.py
import pygame
import sys
import random
import os

from src.entities.configuracoes import Configuracoes
from src.entities.jogador import Jogador
from src.entities.projetil import Projetil
from src.entities.inimigolento import InimigoLento
from src.entities.inimigorapido import InimigoRapido

class Jogo:
    def __init__(self):
        # Inicializa o jogo e seus recursos
        pygame.init()
        
        self.settings = Configuracoes()
        self.tela = pygame.display.set_mode(
            (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA)
        )
        # nome do jogo
        pygame.display.set_caption("Guerra Estelar")
        
        self.clock = pygame.time.Clock()
        
        # no caso de utilizar fonte personalizada
        caminho_fonte = os.path.join('assets', 'fonts', 'sua_fonte_pixel.ttf')
        try:
            self.fonte_grande = pygame.font.Font(caminho_fonte, 60)
            self.fonte_pequena = pygame.font.Font(caminho_fonte, 32)
        except FileNotFoundError:
            print(f"AVISO: Arquivo de fonte não encontrado. Usando fonte padrão.")
            self.fonte_grande = pygame.font.Font(None, 74)
            self.fonte_pequena = pygame.font.Font(None, 40)

        self._carregar_imagens()
        
        self.estado_jogo = 'TELA_INICIAL'

    def rodar_jogo(self):
        # Loop principal
        while True:
            if self.estado_jogo == 'TELA_INICIAL':
                self._rodar_tela_inicial()
            elif self.estado_jogo == 'JOGANDO':
                self._rodar_partida()
            elif self.estado_jogo == 'FIM_DE_JOGO':
                self._rodar_fim_de_jogo()

    def _rodar_tela_inicial(self):
        # Controla o loop da tela inicial
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.estado_jogo = 'JOGANDO'
                    self._iniciar_nova_partida()

        self.tela.blit(self.fundo_inicial_img, (0, 0))
        self._desenhar_texto("Guerra Estelar", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 50)
        self._desenhar_texto("Pressione ESPAÇO para iniciar", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA * 0.75)
        
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _rodar_partida(self):
        # Controla o loop da partida
        self._checar_eventos_partida()
        self._atualizar_sprites()
        self._atualizar_tela_partida()

    def _rodar_fim_de_jogo(self):
        """Controla o loop da tela de fim de jogo."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.estado_jogo = 'TELA_INICIAL'

        self.tela.fill(self.settings.COR_DE_FUNDO)
        self._desenhar_texto("FIM DE JOGO", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 100)
        self._desenhar_texto(f"Pontuação Final: {self.pontuacao}", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2)
        self._desenhar_texto("Pressione 'R' para reiniciar", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 + 50)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _iniciar_nova_partida(self):
        # Prepara os objetos para uma nova partida
        self.pontuacao = 0
        self.all_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.projetis = pygame.sprite.Group()
        self.jogador = Jogador()
        self.all_sprites.add(self.jogador)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def _checar_eventos_partida(self):
        # Verifica eventos durante a partida
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self._disparar_projetil()
            elif evento.type == pygame.USEREVENT:
                self._criar_inimigo()
    
    def _atualizar_sprites(self):
        self.all_sprites.update()
        colisoes = pygame.sprite.groupcollide(self.projetis, self.inimigos, True, True)
        if colisoes:
            self.pontuacao += 10

        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.estado_jogo = 'FIM_DE_JOGO'

    def _atualizar_tela_partida(self):
        """Desenha a tela durante a partida."""
        self.tela.fill(self.settings.COR_DE_FUNDO)
        self.all_sprites.draw(self.tela)
        self._desenhar_texto(f"Pontos: {self.pontuacao}", self.fonte_pequena, 80, 25)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _disparar_projetil(self):
        novo_projetil = Projetil(self.jogador.rect.centerx, self.jogador.rect.top)
        self.all_sprites.add(novo_projetil)
        self.projetis.add(novo_projetil)

    def _criar_inimigo(self):
        if random.choice([True, False]):
            inimigo = InimigoLento()
        else:
            inimigo = InimigoRapido()
        self.all_sprites.add(inimigo)
        self.inimigos.add(inimigo)
        
    def _carregar_imagens(self):
        # Carrega os arquivos de imagem
        try:
            fundo_path = os.path.join('assets', 'images', 'fundo_inicial.jpg')
            self.fundo_inicial_img = pygame.image.load(fundo_path).convert()
            self.fundo_inicial_img = pygame.transform.scale(self.fundo_inicial_img, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
        except pygame.error as e:
            print(f"ERRO: Imagem de fundo não encontrada em '{fundo_path}'.")
            pygame.quit()
            sys.exit()

    def _desenhar_texto(self, texto, fonte, pos_x, pos_y, cor=(255, 255, 255)):
        surface_texto = fonte.render(texto, True, cor)
        rect_texto = surface_texto.get_rect(center=(pos_x, pos_y))
        self.tela.blit(surface_texto, rect_texto)

if __name__ == '__main__':
    meu_jogo = Jogo()
    meu_jogo.rodar_jogo()