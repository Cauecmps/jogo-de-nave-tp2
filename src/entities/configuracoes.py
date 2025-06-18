# src/entities/configuracoes.py
class Configuracoes:
    """Uma classe para armazenar todas as configurações do jogo."""

    def __init__(self):
        """Inicializa as configurações do jogo."""
        # Configurações da tela
        self.LARGURA_TELA = 800
        self.ALTURA_TELA = 600
        self.COR_DE_FUNDO = (0, 0, 0) # Preto
        self.FPS = 60

        # Configurações do jogador
        self.JOGADOR_VELOCIDADE = 5

        # Configurações do projétil
        self.PROJETIL_VELOCIDADE = -10 # Negativo para ir para cima
        self.PROJETIL_COR = (255, 255, 0) # Amarelo

        # Configurações dos Inimigos
        # Soldado (Lento)
        self.SOLDADO_VELOCIDADE_MIN = 1
        self.SOLDADO_VELOCIDADE_MAX = 3
        self.SOLDADO_COR = (0, 0, 255) # Azul

        # General (Rápido)
        self.GENERAL_VELOCIDADE_MIN = 4
        self.GENERAL_VELOCIDADE_MAX = 8
        self.GENERAL_COR = (255, 0, 0) # Vermelho