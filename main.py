# main.py
import pygame
import sys
import random

# ALTERADO: Imports padronizados para o diretório 'src'
from src.entities.configuracoes import Configuracoes
from src.entities.jogador import Jogador
from src.entities.projetil import Projetil
from src.entities.inimigolento import InimigoLento 
from src.entities.inimigorapido import InimigoRapido # ALTERADO: Importa a classe diretamente

class Jogo:
    def __init__(self):
        """Inicializa o jogo e seus recursos."""
        pygame.init()
        self.settings = Configuracoes()

        self.tela = pygame.display.set_mode(
            (self.settings.LARGURA_TELA, self.settings.ALTURA_TELA)
        )
        pygame.display.set_caption("Jogo de Nave")

        self.clock = pygame.time.Clock()
        self.pontuacao = 0

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.projetis = pygame.sprite.Group()

        # Instancia o jogador
        self.jogador = Jogador()
        self.jogador.velocidade = self.settings.JOGADOR_VELOCIDADE # Usa a configuração
        self.all_sprites.add(self.jogador)

        # Timer para criar inimigos
        pygame.time.set_timer(pygame.USEREVENT, 1000) # Cria um inimigo a cada 1 segundo

    def rodar_jogo(self):
        """Inicia o loop principal do jogo."""
        while True:
            self._checar_eventos()
            self._atualizar_sprites()
            self._atualizar_tela()

    def _checar_eventos(self):
        """Responde a eventos de teclado e mouse."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self._disparar_projetil()
            elif evento.type == pygame.USEREVENT:
                self._criar_inimigo()

    def _disparar_projetil(self):
        """Cria um novo projétil e o adiciona ao grupo de projéteis."""
        novo_projetil = Projetil(self.jogador.rect.centerx, self.jogador.rect.top)
        novo_projetil.velocidade = self.settings.PROJETIL_VELOCIDADE
        novo_projetil.image.fill(self.settings.PROJETIL_COR)
        self.all_sprites.add(novo_projetil)
        self.projetis.add(novo_projetil)

    def _criar_inimigo(self):
        """Cria um novo inimigo (Soldado ou InimigoRapido) aleatoriamente."""
        if random.choice([True, False]):
            inimigo = InimigoLento()
            inimigo.velocidade = random.randint(
                self.settings.INIMIGOLENTO_VELOCIDADE_MIN, self.settings.INIMIGOLENTO_VELOCIDADE_MAX
            )
            inimigo.image.fill(self.settings.INIMIGOLENTO_COR)
        else:
            # ALTERADO: Instancia a classe InimigoRapido diretamente
            inimigo = InimigoRapido() 
            # ALTERADO: Usa as configurações de InimigoRapido
            inimigo.velocidade = random.randint(
                self.settings.INIMIGO_RAPIDO_VELOCIDADE_MIN, self.settings.INIMIGO_RAPIDO_VELOCIDADE_MAX
            )
            inimigo.image.fill(self.settings.INIMIGO_RAPIDO_COR)
        
        self.all_sprites.add(inimigo)
        self.inimigos.add(inimigo)

    def _atualizar_sprites(self):
        """Atualiza a posição dos sprites e verifica colisões."""
        self.all_sprites.update()

        # Verifica colisão de projéteis com inimigos
        colisoes = pygame.sprite.groupcollide(self.projetis, self.inimigos, True, True)
        if colisoes:
            self.pontuacao += 10
            print(f"Pontuação: {self.pontuacao}") # Exibe a pontuação no console

        # Verifica colisão do jogador com inimigos
        if pygame.sprite.spritecollide(self.jogador, self.inimigos, False):
            print("Fim de Jogo!")
            pygame.quit()
            sys.exit()


    def _atualizar_tela(self):
        """Atualiza os objetos na tela."""
        self.tela.fill(self.settings.COR_DE_FUNDO)
        self.all_sprites.draw(self.tela)
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

if __name__ == '__main__':
    # Cria uma instância do jogo e o executa.
    meu_jogo = Jogo()
    meu_jogo.rodar_jogo()