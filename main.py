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

        # Fontes padrão para o jogo
        self.fonte_grande = pygame.font.Font(None, 74)
        self.fonte_pequena = pygame.font.Font(None, 40)

        # Tenta carregar a fonte personalizada para a tela inicial
        try:
            caminho_fonte_inicial = os.path.join('assets', 'fonts', 'font2p.ttf')
            self.fonte_inicial_grande = pygame.font.Font(caminho_fonte_inicial, 50)
            # --- ALTERADO: Tamanho da fonte menor para caber na tela ---
            self.fonte_inicial_pequena = pygame.font.Font(caminho_fonte_inicial, 25) 
        except pygame.error:
            print("AVISO: Fonte 'font2p.ttf' não encontrada, usando fonte padrão para a tela inicial.")
            self.fonte_inicial_grande = self.fonte_grande
            self.fonte_inicial_pequena = self.fonte_pequena

        self._carregar_imagens()
        self._carregar_sons()
        
        self.estado_jogo = 'TELA_INICIAL'
        self.opcoes_fim_de_jogo = ['Reiniciar', 'Sair']
        self.opcao_selecionada = 0
        
        self.fullscreen = False

        # --- ADICIONADO: Variáveis para o texto piscar ---
        self.texto_inicial_visivel = True
        self.timer_piscar = pygame.time.get_ticks()

    def rodar_jogo(self):
        """Loop principal que controla os estados do jogo."""
        while True:
            eventos = pygame.event.get()
            self._processar_eventos(eventos)
            self._atualizar_logica()
            self._desenhar_tela()

    def _processar_eventos(self, eventos):
        """Gerencia TODOS os eventos do jogo, independente do estado."""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    self._toggle_fullscreen()

            if self.estado_jogo == 'TELA_INICIAL':
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    self.estado_jogo = 'JOGANDO'
                    self._iniciar_nova_partida()
            
            elif self.estado_jogo == 'JOGANDO':
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    self._disparar_projetil()
                elif evento.type == pygame.USEREVENT:
                    self._criar_inimigo()

            elif self.estado_jogo == 'FIM_DE_JOGO':
                self._processar_eventos_fim_de_jogo(evento)

    def _atualizar_logica(self):
        """Atualiza o estado dos objetos"""
        # --- ADICIONADO: Lógica para o texto piscar ---
        if self.estado_jogo == 'TELA_INICIAL':
            agora = pygame.time.get_ticks()
            # A cada 700ms, inverte a visibilidade do texto
            if agora - self.timer_piscar > 700:
                self.texto_inicial_visivel = not self.texto_inicial_visivel
                self.timer_piscar = agora

        elif self.estado_jogo == 'JOGANDO':
            self.all_sprites.update()
            
            colisoes = pygame.sprite.groupcollide(self.projetis, self.inimigos, True, True)
            if colisoes:
                self.pontuacao += 10
                self.som_explosao.play()

            if self.mapa_atual == 1 and self.pontuacao >= self.settings.PONTOS_PARA_PROXIMO_MAPA:
                self.estado_jogo = 'LEVEL_UP'
                self.level_up_timer = pygame.time.get_ticks()

            if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
                self.estado_jogo = 'FIM_DE_JOGO'
                pygame.mixer.music.stop()

        elif self.estado_jogo == 'LEVEL_UP':
            agora = pygame.time.get_ticks()
            if agora - self.level_up_timer > self.settings.DURACAO_LEVEL_UP_MS:
                self.mapa_atual = 2
                self.fundo_ativo = self.fundo_mapa_2
                self.estado_jogo = 'JOGANDO'

    def _desenhar_tela(self):
        """Desenha tudo na tela com base no estado atual do jogo."""
        if self.estado_jogo == 'TELA_INICIAL':
            self.tela.blit(self.fundo_inicial_img, (0, 0))
            self._desenhar_texto("Guerra Estelar", self.fonte_inicial_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 50)
            
            # --- ALTERADO: Desenha o texto apenas se ele estiver visível ---
            if self.texto_inicial_visivel:
                self._desenhar_texto("Pressione ESPAÇO para iniciar", self.fonte_inicial_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA * 0.75)
        
        elif self.estado_jogo == 'JOGANDO':
            self.tela.blit(self.fundo_ativo, (0, 0))
            self.all_sprites.draw(self.tela)
            self._desenhar_texto(f"Pontos: {self.pontuacao}", self.fonte_pequena, 80, 25)
        
        elif self.estado_jogo == 'LEVEL_UP':
            self.tela.blit(self.fundo_ativo, (0, 0))
            self.all_sprites.draw(self.tela)
            self._desenhar_texto("NOVO NÍVEL!", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2)

        elif self.estado_jogo == 'FIM_DE_JOGO':
            self.tela.fill(self.settings.COR_DE_FUNDO)
            self._desenhar_texto("Game Over", self.fonte_grande, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 4)
            self._desenhar_texto(f"Pontuação Final: {self.pontuacao}", self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 - 50)
            self._desenhar_opcoes_menu()

        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
    
    def _processar_eventos_fim_de_jogo(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes_fim_de_jogo)
            elif evento.key == pygame.K_DOWN:
                self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes_fim_de_jogo)
            elif evento.key == pygame.K_RETURN:
                if self.opcoes_fim_de_jogo[self.opcao_selecionada] == 'Reiniciar':
                    self.estado_jogo = 'TELA_INICIAL'
                elif self.opcoes_fim_de_jogo[self.opcao_selecionada] == 'Sair':
                    pygame.quit()
                    sys.exit()

    def _desenhar_opcoes_menu(self):
        for i, opcao in enumerate(self.opcoes_fim_de_jogo):
            cor = (255, 255, 0) if i == self.opcao_selecionada else (255, 255, 255)
            self._desenhar_texto(opcao, self.fonte_pequena, self.settings.LARGURA_TELA / 2, self.settings.ALTURA_TELA / 2 + 50 + i * 50, cor)

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
        pygame.mixer.music.play(loops=-1)

    def _disparar_projetil(self):
        novo_projetil = Projetil(self.jogador.rect.centerx, self.jogador.rect.top)
        self.all_sprites.add(novo_projetil)
        self.projetis.add(novo_projetil)
        self.som_tiro.play()

    def _criar_inimigo(self):
        if random.choice([True, False]):
            inimigo = InimigoLento()
        else:
            inimigo = InimigoRapido()
        self.all_sprites.add(inimigo)
        self.inimigos.add(inimigo)
        
    def _carregar_imagens(self):
        try:
            fundo_inicial = os.path.join('assets', 'images', 'fundo_inicial.jpg')
            self.fundo_inicial_img = pygame.image.load(fundo_inicial).convert()
            self.fundo_inicial_img = pygame.transform.scale(self.fundo_inicial_img, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
            
            fundo_1 = os.path.join('assets', 'images', 'fundo_mapa_1.jpg')
            self.fundo_mapa_1 = pygame.image.load(fundo_1).convert()
            self.fundo_mapa_1 = pygame.transform.scale(self.fundo_mapa_1, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
            
            fundo_2 = os.path.join('assets', 'images', 'fundo_mapa_2.png')
            self.fundo_mapa_2 = pygame.image.load(fundo_2).convert_alpha()
            self.fundo_mapa_2 = pygame.transform.scale(self.fundo_mapa_2, (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))
        except pygame.error as e:
            print(f"Uma ou mais imagens de fundo não foram encontradas.")
            print(e)
            pygame.quit()
            sys.exit()

    def _carregar_sons(self):
        """Carrega os arquivos de áudio do jogo."""
        try:
            caminho_musica = os.path.join('assets', 'sounds', 'musica_fundo.mp3')
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.3)

            caminho_tiro = os.path.join('assets', 'sounds', 'tiro.wav')
            self.som_tiro = pygame.mixer.Sound(caminho_tiro)
            
            caminho_explosao = os.path.join('assets', 'sounds', 'explosao.wav')
            self.som_explosao = pygame.mixer.Sound(caminho_explosao)
        except pygame.error as e:
            print(f"Erro ao carregar um arquivo de som: {e}")

    def _desenhar_texto(self, texto, fonte, pos_x, pos_y, cor=(255, 255, 255)):
        surface_texto = fonte.render(texto, True, cor)
        rect_texto = surface_texto.get_rect(center=(pos_x, pos_y))
        self.tela.blit(surface_texto, rect_texto)

    def _toggle_fullscreen(self):
        """Alterna entre o modo de tela cheia e o modo janela."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.tela = pygame.display.set_mode((self.settings.LARGURA_TELA, self.settings.ALTURA_TELA), pygame.FULLSCREEN)
        else:
            self.tela = pygame.display.set_mode((self.settings.LARGURA_TELA, self.settings.ALTURA_TELA))


if __name__ == '__main__':
    meu_jogo = Jogo()
    meu_jogo.rodar_jogo()