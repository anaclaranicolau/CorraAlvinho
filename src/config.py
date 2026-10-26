"""
Configurações globais e constantes do jogo Corra, Alvinho!
"""
import os

# Dimensões da janela
LARGURA = 900
ALTURA = 500
TITULO = "Corra, Alvinho! - Corrida Infinita"
FPS = 60

# Diretórios
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_ASSETS = os.path.join(DIRETORIO_RAIZ, "assets")
DIRETORIO_SPRITES = os.path.join(DIRETORIO_ASSETS, "sprites")
DIRETORIO_SOUNDS = os.path.join(DIRETORIO_ASSETS, "sounds")
ARQUIVO_HIGHSCORE = os.path.join(DIRETORIO_RAIZ, "highscore.json")

# Chão e Física
ALTURA_CHAO = 95
Y_CHAO = ALTURA - ALTURA_CHAO

GRAVIDADE = 0.82
GRAVIDADE_PULO_ALTO = 0.52   # Quando segura o botão para pular mais alto
FORCA_PULO = -14.8

# Velocidade do jogo
VELOCIDADE_INICIAL = 6.8
VELOCIDADE_MAXIMA = 24.0
ACELERACAO_VELOCIDADE = 0.0025  # Aceleração progressiva mais intensa por frame

# Cores
BRANCO = (255, 255, 255)
PRETO = (25, 25, 30)
CINZA_ESCURO = (50, 55, 65)
CINZA_CLARO = (210, 215, 225)
AZUL_CEU_DIA = (160, 210, 255)
AZUL_CEU_NOITE = (18, 22, 45)
AMARELO_OURO = (255, 215, 40)
LARANJA = (255, 130, 45)
VERDE_GRAMA = (76, 175, 80)
VERDE_ESCURO = (45, 120, 50)
VERMELHO_CORACAO = (235, 65, 75)
ROXO_SUAVE = (130, 80, 200)

# Pontuações
PONTOS_PETISCO = 100
PONTOS_BRINQUEDO = 250
INTERVALO_MILESTONE = 500  # Dino beep a cada 100 pontos
