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
        pygame.init()
        self.settings = Configuracoes()
        self.tela = pygame.display.set_mode(
            (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA)
        )
        pygame.display.set_caption("Guerra Estelar")
        self.clock = pygame.time.Clock()
        self.fonte_grande = pygame.font.Font(None, 74)
        self.fonte_pequena = pygame.font.Font(None, 40)
        
        self._carregar_imagens()
        
        self.estado_jogo = 'TELA_INICIAL'

    def rodar_jogo(self):
        while True:
            # O fluxo principal agora lida com o novo estado
            if self.estado_jogo == 'TELA_INICIAL':
                self._rodar_tela_inicial()
            elif self.estado_jogo == 'JOGANDO':
                self._rodar_partida()
            # NOVO: Adiciona o estado de level up
            elif self.estado_jogo == 'LEVEL_UP':
                self._rodar_level_up()
            elif self.estado_jogo == 'FIM_DE_JOGO':
                self._rodar_fim_de_jogo()

    def _rodar_tela_inicial(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.estado_jogo = 'JOGANDO'
                self._iniciar_nova_partida()

        self.tela.blit(self.fundo_inicial_img, (0, 0))
        self._desenhar_texto("Guerra Estelar", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 50)
        self._desenhar_texto("Pressione ESPAÇO para iniciar", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA * 0.75)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _rodar_partida(self):
        self._checar_eventos_partida()
        self._atualizar_sprites()
        self._atualizar_tela_partida()
        
    def _rodar_level_up(self):
        """NOVO: Pausa o jogo e mostra a mensagem de level up."""
        # Desenha a tela da partida por baixo, mas sem atualizar os sprites
        self.tela.blit(self.fundo_ativo, (0, 0))
        self.all_sprites.draw(self.tela)
        self._desenhar_texto(f"Pontos: {self.pontuacao}", self.fonte_pequena, 80, 25)

        # Desenha a mensagem por cima
        self._desenhar_texto("NOVO NÍVEL!", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2)
        pygame.display.flip()

        # Verifica se o tempo da pausa já passou
        agora = pygame.time.get_ticks()
        if agora - self.level_up_timer > self.settings.DURACAO_LEVEL_UP_MS:
            # Troca o mapa e volta a jogar
            self.mapa_atual = 2
            self.fundo_ativo = self.fundo_mapa_2
            self.estado_jogo = 'JOGANDO'

    def _rodar_fim_de_jogo(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.estado_jogo = 'TELA_INICIAL'

        self.tela.fill(self.settings.COR_DE_FUNDO)
        self._desenhar_texto("FIM DE JOGO", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 100)
        self._desenhar_texto(f"Pontuação Final: {self.pontuacao}", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2)
        self._desenhar_texto("Pressione 'R' para reiniciar", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 + 50)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _iniciar_nova_partida(self):
        self.pontuacao = 0
        self.mapa_atual = 1
        self.fundo_ativo = self.fundo_mapa_1
        self.all_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.projetis = pygame.sprite.Group()
        self.jogador = Jogador()
        self.all_sprites.add(self.jogador)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def _checar_eventos_partida(self):
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

        # ALTERADO: Lógica para iniciar o level up
        if self.mapa_atual == 1 and self.pontuacao >= self.settings.PONTOS_PARA_PROXIMO_MAPA:
            self.estado_jogo = 'LEVEL_UP'
            # NOVO: Inicia o timer para a pausa
            self.level_up_timer = pygame.time.get_ticks()

        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.estado_jogo = 'FIM_DE_JOGO'

    def _atualizar_tela_partida(self):
        self.tela.blit(self.fundo_ativo, (0, 0))
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
        try:
            fundo_path_inicial = os.path.join('assets', 'images', 'fundo_inicial.jpg')
            self.fundo_inicial_img = pygame.image.load(fundo_path_inicial).convert()
            self.fundo_inicial_img = pygame.transform.scale(self.fundo_inicial_img, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
            
            fundo_path_1 = os.path.join('assets', 'images', 'fundo_mapa_1.jpg')
            self.fundo_mapa_1 = pygame.image.load(fundo_path_1).convert()
            self.fundo_mapa_1 = pygame.transform.scale(self.fundo_mapa_1, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
            
            fundo_path_2 = os.path.join('assets', 'images', 'fundo_mapa_2.png')
            self.fundo_mapa_2 = pygame.image.load(fundo_path_2).convert_alpha()
            self.fundo_mapa_2 = pygame.transform.scale(self.fundo_mapa_2, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
            
        except pygame.error as e:
            print(f"ERRO: Imagem de fundo não encontrada. Verifique a pasta 'assets/images'.")
            print(e)
            pygame.quit()
            sys.exit()

    def _desenhar_texto(self, texto, fonte, pos_x, pos_y, cor=(255, 255, 255)):
        surface_texto = fonte.render(texto, True, cor)
        rect_texto = surface_texto.get_rect(center=(pos_x, pos_y))
        self.tela.blit(surface_texto, rect_texto)

if __name__ == '__main__':
    meu_jogo = Jogo()
    meu_jogo.rodar_jogo()