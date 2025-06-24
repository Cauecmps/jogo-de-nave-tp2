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
        pygame.mixer.init() 
        
        self.settings = Configuracoes()
        self.tela = pygame.display.set_mode(
            (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA)
        )
        pygame.display.set_caption("Guerra Estelar")
        self.clock = pygame.time.Clock()
        
        try:
            caminho_fonte = os.path.join('assets', 'fonts', 'sua_fonte_pixel.ttf')
            self.fonte_grande = pygame.font.Font(caminho_fonte, 60)
            self.fonte_pequena = pygame.font.Font(caminho_fonte, 32)
        except FileNotFoundError:
            self.fonte_grande = pygame.font.Font(None, 74)
            self.fonte_pequena = pygame.font.Font(None, 40)

        self._carregar_midia()
        
        self.estado_jogo = 'TELA_INICIAL'

    def rodar_jogo(self):
        while True:
            if self.estado_jogo == 'TELA_INICIAL':
                self._rodar_tela_inicial()
            elif self.estado_jogo == 'JOGANDO':
                self._rodar_partida()
            elif self.estado_jogo == 'FIM_DE_JOGO':
                self._rodar_fim_de_jogo()

    def _rodar_tela_inicial(self):
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
        self._checar_eventos_partida()
        self._atualizar_sprites()
        self._atualizar_tela_partida()

    def _rodar_fim_de_jogo(self):
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
        self.pontuacao = 0
        self.all_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.projetis = pygame.sprite.Group()
        self.jogador = Jogador()
        self.all_sprites.add(self.jogador)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        if self.musica_carregada:
            pygame.mixer.music.play(loops=-1)

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
            self.som_explosao.play()

        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.estado_jogo = 'FIM_DE_JOGO'
            pygame.mixer.music.stop()

    def _atualizar_tela_partida(self):
        self.tela.fill(self.settings.COR_DE_FUNDO)
        self.all_sprites.draw(self.tela)
        self._desenhar_texto(f"Pontos: {self.pontuacao}", self.fonte_pequena, 80, 25)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _disparar_projetil(self):
        self.som_tiro.play()
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
        
    def _carregar_midia(self):
        # Carregar imagem de fundo
        try:
            fundo_path = os.path.join('assets', 'images', 'fundo_inicial.jpg')
            self.fundo_inicial_img = pygame.image.load(fundo_path).convert()
            self.fundo_inicial_img = pygame.transform.scale(self.fundo_inicial_img, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
        except pygame.error as e:
            print(f"ERRO ao carregar imagem de fundo: {e}")
            self.fundo_inicial_img = pygame.Surface(self.tela.get_size()).convert()
            self.fundo_inicial_img.fill((0, 0, 0))

        # Carregar sons e música
        self.musica_carregada = False
        class SomFalso:
            def play(self): pass
        self.som_tiro = SomFalso()
        self.som_explosao = SomFalso()
        
        try:
            # ALTERADO: Carrega o arquivo .mp3
            pygame.mixer.music.load(os.path.join('assets', 'sounds', 'musica_fundo.mp3'))
            pygame.mixer.music.set_volume(0.4)
            self.som_tiro = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'tiro.wav'))
            self.som_explosao = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosao.wav'))
            self.musica_carregada = True
        except pygame.error as e:
            print(f"AVISO: Um ou mais arquivos de áudio não encontrados. O jogo pode rodar com som parcial. ({e})")

    def _desenhar_texto(self, texto, fonte, pos_x, pos_y, cor=(255, 255, 255)):
        surface_texto = fonte.render(texto, True, cor)
        rect_texto = surface_texto.get_rect(center=(pos_x, pos_y))
        self.tela.blit(surface_texto, rect_texto)

if __name__ == '__main__':
    meu_jogo = Jogo()
    meu_jogo.rodar_jogo()