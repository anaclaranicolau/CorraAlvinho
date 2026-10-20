import pygame
import random

pygame.init()

# Janela
LARGURA = 900
ALTURA = 500

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corre, Alvinho!")

RELOGIO = pygame.time.Clock()
FPS = 60

# Cores
AZUL_CLARO = (190, 225, 255)
VERDE = (100, 190, 100)
BRANCO = (255, 255, 255)
PRETO = (30, 30, 30)
VERMELHO = (210, 70, 70)
AMARELO = (255, 210, 50)

# Fontes
FONTE_GRANDE = pygame.font.Font(None, 65)
FONTE_MEDIA = pygame.font.Font(None, 38)
FONTE_PEQUENA = pygame.font.Font(None, 28)

# Chão
ALTURA_CHAO = 80
Y_CHAO = ALTURA - ALTURA_CHAO


class Alvinho:
    def __init__(self):
        self.largura = 110
        self.altura = 85

        self.x = 120
        self.y = Y_CHAO - self.altura

        self.velocidade_y = 0
        self.forca_pulo = -15
        self.gravidade = 0.8

        self.no_chao = True
        self.derrotado = False

        # Controle da animação
        self.frame_atual = 0
        self.tempo_animacao = 0
        self.velocidade_animacao = 8

        self.sprite_sheet = pygame.image.load(
            "assets/alvinho_sprites.png"
        ).convert_alpha()

        self.frames = self.separar_frames()

    def separar_frames(self):
        frames = []

        largura_folha = self.sprite_sheet.get_width()
        altura_folha = self.sprite_sheet.get_height()
        largura_frame = largura_folha // 4

        for i in range(4):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(
                    i * largura_frame,
                    0,
                    largura_frame,
                    altura_folha
                )
            )

            frame = pygame.transform.smoothscale(
                frame,
                (self.largura, self.altura)
            )

            frames.append(frame)

        return frames

    def pular(self):
        if self.no_chao and not self.derrotado:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def atualizar(self):
        if self.derrotado:
            return

        self.velocidade_y += self.gravidade
        self.y += self.velocidade_y

        if self.y >= Y_CHAO - self.altura:
            self.y = Y_CHAO - self.altura
            self.velocidade_y = 0
            self.no_chao = True

        if self.no_chao:
            self.tempo_animacao += 1

            if self.tempo_animacao >= self.velocidade_animacao:
                self.frame_atual = 1 - self.frame_atual
                self.tempo_animacao = 0

    def desenhar(self, tela):
        if self.derrotado:
            imagem = self.frames[3]

        elif not self.no_chao:
            imagem = self.frames[2]

        else:
            imagem = self.frames[self.frame_atual]

        tela.blit(imagem, (self.x, self.y))

    def colisao(self):
        return pygame.Rect(
            self.x + 18,
            self.y + 10,
            self.largura - 36,
            self.altura - 15
        )


class Obstaculo:
    def __init__(self, velocidade):
        self.tipo = random.choice(
            ["banheira", "shampoo"]
        )

        self.velocidade = velocidade
        self.x = LARGURA

        sprite_sheet = pygame.image.load(
            "assets/obstaculos.png"
        ).convert_alpha()

        largura_folha = sprite_sheet.get_width()
        altura_folha = sprite_sheet.get_height()
        largura_frame = largura_folha // 2

        if self.tipo == "banheira":
            imagem = sprite_sheet.subsurface(
                pygame.Rect(
                    0,
                    0,
                    largura_frame,
                    altura_folha
                )
            )

            self.largura = 95
            self.altura = 65

        else:
            imagem = sprite_sheet.subsurface(
                pygame.Rect(
                    largura_frame,
                    0,
                    largura_frame,
                    altura_folha
                )
            )

            self.largura = 55
            self.altura = 75

        self.imagem = pygame.transform.smoothscale(
            imagem,
            (self.largura, self.altura)
        )

        self.y = Y_CHAO - self.altura

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(
            self.imagem,
            (self.x, self.y)
        )

    def colisao(self):
        if self.tipo == "banheira":
            return pygame.Rect(
                self.x + 8,
                self.y + 15,
                self.largura - 16,
                self.altura - 15
            )

        return pygame.Rect(
            self.x + 10,
            self.y + 8,
            self.largura - 20,
            self.altura - 8
        )

    def saiu_da_tela(self):
        return self.x + self.largura < 0


class Colecionavel:
    def __init__(self, velocidade):
        self.tipo = random.choice(
            ["petisco", "brinquedo"]
        )

        self.velocidade = velocidade
        self.x = LARGURA

        sprite_sheet = pygame.image.load(
            "assets/colecionaveis.png"
        ).convert_alpha()

        largura_folha = sprite_sheet.get_width()
        altura_folha = sprite_sheet.get_height()
        largura_frame = largura_folha // 2

        if self.tipo == "petisco":
            imagem = sprite_sheet.subsurface(
                pygame.Rect(
                    0,
                    0,
                    largura_frame,
                    altura_folha
                )
            )

            self.largura = 55
            self.altura = 40
            self.valor = 10

        else:
            imagem = sprite_sheet.subsurface(
                pygame.Rect(
                    largura_frame,
                    0,
                    largura_frame,
                    altura_folha
                )
            )

            self.largura = 45
            self.altura = 45
            self.valor = 25

        self.imagem = pygame.transform.smoothscale(
            imagem,
            (self.largura, self.altura)
        )

        # Alguns itens aparecem no chão e outros no alto
        altura_item = random.choice(
            [15, 75, 120]
        )

        self.y = Y_CHAO - self.altura - altura_item

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(
            self.imagem,
            (self.x, self.y)
        )

    def colisao(self):
        return pygame.Rect(
            self.x + 5,
            self.y + 5,
            self.largura - 10,
            self.altura - 10
        )

    def saiu_da_tela(self):
        return self.x + self.largura < 0


def escrever(texto, fonte, cor, x, y, centralizado=False):
    imagem_texto = fonte.render(
        texto,
        True,
        cor
    )

    if centralizado:
        retangulo_texto = imagem_texto.get_rect(
            center=(x, y)
        )

    else:
        retangulo_texto = imagem_texto.get_rect(
            topleft=(x, y)
        )

    TELA.blit(
        imagem_texto,
        retangulo_texto
    )


def novo_jogo():
    alvinho = Alvinho()

    obstaculos = []
    colecionaveis = []

    pontuacao = 0
    velocidade = 7

    tempo_obstaculo = 0
    proximo_obstaculo = random.randint(80, 130)

    tempo_colecionavel = 0
    proximo_colecionavel = random.randint(100, 180)

    return (
        alvinho,
        obstaculos,
        colecionaveis,
        pontuacao,
        velocidade,
        tempo_obstaculo,
        proximo_obstaculo,
        tempo_colecionavel,
        proximo_colecionavel
    )


(
    alvinho,
    obstaculos,
    colecionaveis,
    pontuacao,
    velocidade,
    tempo_obstaculo,
    proximo_obstaculo,
    tempo_colecionavel,
    proximo_colecionavel
) = novo_jogo()

estado = "inicio"
executando = True


while executando:
    RELOGIO.tick(FPS)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:

                if estado == "inicio":
                    estado = "jogando"
                    alvinho.pular()

                elif estado == "jogando":
                    alvinho.pular()

                elif estado == "game_over":
                    (
                        alvinho,
                        obstaculos,
                        colecionaveis,
                        pontuacao,
                        velocidade,
                        tempo_obstaculo,
                        proximo_obstaculo,
                        tempo_colecionavel,
                        proximo_colecionavel
                    ) = novo_jogo()

                    estado = "jogando"

    # Atualização
    if estado == "jogando":
        alvinho.atualizar()

        tempo_obstaculo += 1
        tempo_colecionavel += 1

        # Cria obstáculos
        if tempo_obstaculo >= proximo_obstaculo:
            obstaculos.append(
                Obstaculo(velocidade)
            )

            tempo_obstaculo = 0
            proximo_obstaculo = random.randint(80, 130)

        # Cria itens colecionáveis
        if tempo_colecionavel >= proximo_colecionavel:
            colecionaveis.append(
                Colecionavel(velocidade)
            )

            tempo_colecionavel = 0
            proximo_colecionavel = random.randint(100, 180)

        # Atualiza obstáculos
        for obstaculo in obstaculos:
            obstaculo.velocidade = velocidade
            obstaculo.atualizar()

            if alvinho.colisao().colliderect(
                obstaculo.colisao()
            ):
                alvinho.derrotado = True
                estado = "game_over"

        # Atualiza colecionáveis
        for item in colecionaveis[:]:
            item.velocidade = velocidade
            item.atualizar()

            if alvinho.colisao().colliderect(
                item.colisao()
            ):
                if item.tipo == "petisco":
                    pontuacao += 100

                else:
                    pontuacao += 250

                colecionaveis.remove(item)

        # Remove obstáculos fora da tela
        obstaculos = [
            obstaculo
            for obstaculo in obstaculos
            if not obstaculo.saiu_da_tela()
        ]

        # Remove colecionáveis fora da tela
        colecionaveis = [
            item
            for item in colecionaveis
            if not item.saiu_da_tela()
        ]

        # Pontos pelo tempo sobrevivido
        pontuacao += 1

        # Aumenta a dificuldade
        velocidade = 7 + pontuacao // 600

    # Fundo
    TELA.fill(AZUL_CLARO)

    # Nuvens
    pygame.draw.circle(
        TELA,
        BRANCO,
        (700, 90),
        35
    )

    pygame.draw.circle(
        TELA,
        BRANCO,
        (740, 90),
        45
    )

    pygame.draw.circle(
        TELA,
        BRANCO,
        (780, 90),
        30
    )

    # Chão
    pygame.draw.rect(
        TELA,
        VERDE,
        (
            0,
            Y_CHAO,
            LARGURA,
            ALTURA_CHAO
        )
    )

    # Desenha os colecionáveis
    for item in colecionaveis:
        item.desenhar(TELA)

    # Desenha Alvinho
    alvinho.desenhar(TELA)

    # Desenha obstáculos
    for obstaculo in obstaculos:
        obstaculo.desenhar(TELA)

    # Tela inicial
    if estado == "inicio":
        escrever(
            "CORRE, ALVINHO!",
            FONTE_GRANDE,
            PRETO,
            LARGURA // 2,
            105,
            True
        )

        escrever(
            "Ajude Alvinho a fugir do banho!",
            FONTE_MEDIA,
            PRETO,
            LARGURA // 2,
            170,
            True
        )

        escrever(
            "Pule sobre banheiras e shampoos.",
            FONTE_PEQUENA,
            PRETO,
            LARGURA // 2,
            215,
            True
        )

        escrever(
            "Petisco: +10 pontos | Brinquedo: +25 pontos",
            FONTE_PEQUENA,
            PRETO,
            LARGURA // 2,
            250,
            True
        )

        escrever(
            "ESPAÇO para começar e pular",
            FONTE_MEDIA,
            VERMELHO,
            LARGURA // 2,
            305,
            True
        )

    # Jogo acontecendo
    elif estado == "jogando":
        escrever(
            f"Pontos: {pontuacao // 10}",
            FONTE_MEDIA,
            PRETO,
            25,
            25
        )

    # Tela de derrota
    elif estado == "game_over":
        escrever(
            "ALVINHO FOI PEGO!",
            FONTE_GRANDE,
            VERMELHO,
            LARGURA // 2,
            150,
            True
        )

        escrever(
            f"Pontuação: {pontuacao // 10}",
            FONTE_MEDIA,
            PRETO,
            LARGURA // 2,
            215,
            True
        )

        escrever(
            "ESPAÇO para tentar novamente",
            FONTE_MEDIA,
            PRETO,
            LARGURA // 2,
            265,
            True
        )

    pygame.display.flip()


pygame.quit()