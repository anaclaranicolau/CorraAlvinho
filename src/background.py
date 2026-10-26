"""
Cenário em paralaxe com transição dia/noite e chão dinâmico estilo Chrome Dino.
"""
import math
import random
import pygame
from src.config import LARGURA, ALTURA, Y_CHAO, ALTURA_CHAO, AZUL_CEU_DIA, AZUL_CEU_NOITE, VERDE_GRAMA, VERDE_ESCURO
from src.asset_manager import AssetManager


class Nuvem:
    def __init__(self, x, y, velocidade, escala=1.0):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.escala = escala

    def atualizar(self, vel_jogo):
        self.x -= (self.velocidade + vel_jogo * 0.12)
        if self.x < -180:
            self.x = LARGURA + random.randint(30, 120)
            self.y = random.randint(35, 115)

    def desenhar(self, tela, alpha=150):
        # Nuvem suave semitransparente
        largura_n = int(140 * self.escala)
        altura_n = int(60 * self.escala)
        surf = pygame.Surface((largura_n, altura_n), pygame.SRCALPHA)
        cor = (255, 255, 255, alpha)

        r1 = int(22 * self.escala)
        r2 = int(28 * self.escala)
        r3 = int(20 * self.escala)

        pygame.draw.circle(surf, cor, (int(38 * self.escala), int(36 * self.escala)), r1)
        pygame.draw.circle(surf, cor, (int(70 * self.escala), int(28 * self.escala)), r2)
        pygame.draw.circle(surf, cor, (int(102 * self.escala), int(36 * self.escala)), r3)
        pygame.draw.ellipse(surf, cor, pygame.Rect(int(18 * self.escala), int(26 * self.escala), int(104 * self.escala), int(30 * self.escala)))

        tela.blit(surf, (int(self.x), int(self.y)))


class CenarioParalaxe:
    def __init__(self):
        self.assets = AssetManager()
        self.x_fundo = 0.0
        self.x_chao = 0.0

        # Cria versões espelhadas horizontalmente para ciclo de rolagem contínuo sem costuras visíveis
        self.largura_ciclo_bg = LARGURA * 2
        bg_dia = self.assets.imagens.get("bg_dia")
        if bg_dia:
            self.bg_dia_flip = pygame.transform.flip(bg_dia, True, False)
        else:
            self.bg_dia_flip = None

        bg_noite = self.assets.imagens.get("bg_noite")
        if bg_noite:
            self.bg_noite_flip = pygame.transform.flip(bg_noite, True, False)
        else:
            self.bg_noite_flip = None

        # Transição Dia / Noite estilo Chrome Dino (ocorre a cada ciclo de distância)
        self.fator_noite = 0.0       # 0.0 = Dia total, 1.0 = Noite total
        self.duracao_fase = 900      # frames de dia ou noite (~15 seg)
        self.duracao_transicao = 150 # frames de transição suave
        self.tempo_ciclo = 0

        # Nuvens procedurais suaves
        self.nuvens = [
            Nuvem(100, 45, 0.45, 0.9),
            Nuvem(380, 80, 0.60, 1.1),
            Nuvem(690, 40, 0.40, 0.85),
            Nuvem(980, 70, 0.55, 1.0),
        ]

        # Estrelas piscantes para a noite
        self.estrelas = []
        rng = random.Random(1337)
        for _ in range(45):
            self.estrelas.append({
                "x": rng.randint(0, LARGURA),
                "y": rng.randint(15, Y_CHAO - 90),
                "raio": rng.choice([1, 1, 2]),
                "brilho": rng.uniform(0.3, 1.0),
                "fase": rng.uniform(0, math.pi * 2)
            })

        # Cria textura do chão contínua para rolagem impecável
        self.surf_chao = self._criar_textura_chao()

    def _criar_textura_chao(self):
        # Superfície com 2x a largura da tela para rolagem modular
        largura_textura = LARGURA
        surf = pygame.Surface((largura_textura, ALTURA_CHAO), pygame.SRCALPHA)

        # Camada de terra/base
        cor_terra = (115, 85, 55)
        cor_terra_escura = (90, 65, 40)
        pygame.draw.rect(surf, cor_terra, (0, 0, largura_textura, ALTURA_CHAO))

        # Camada superior de grama viçosa
        altura_grama = 26
        pygame.draw.rect(surf, VERDE_GRAMA, (0, 0, largura_textura, altura_grama))
        # Linha de destaque no topo da grama
        pygame.draw.line(surf, (140, 220, 110), (0, 1), (largura_textura, 1), 2)
        # Sombra abaixo da grama
        pygame.draw.rect(surf, VERDE_ESCURO, (0, altura_grama - 5, largura_textura, 5))

        # Detalhes repetíveis: tufos de grama e pequenas pedrinhas
        rng = random.Random(42)
        for x in range(0, largura_textura, 18):
            # Tufo de grama
            var_x = x + rng.randint(-3, 3)
            h = rng.randint(4, 9)
            pygame.draw.line(surf, (120, 210, 95), (var_x, 0), (var_x - 2, -h + 2), 2)
            pygame.draw.line(surf, (135, 225, 105), (var_x, 0), (var_x + 2, -h + 1), 2)

        # Pedrinhas e textura na terra
        for _ in range(50):
            px = rng.randint(0, largura_textura)
            py = rng.randint(altura_grama + 4, ALTURA_CHAO - 8)
            t = rng.randint(2, 5)
            cor_pedra = rng.choice([cor_terra_escura, (140, 110, 80), (160, 150, 135)])
            pygame.draw.circle(surf, cor_pedra, (px, py), t)

        return surf

    def atualizar(self, velocidade):
        # Atualiza rolagem do fundo (paralaxe suave sem costuras)
        self.x_fundo = (self.x_fundo - velocidade * 0.20) % self.largura_ciclo_bg
        self.x_chao = (self.x_chao - velocidade) % LARGURA

        # Nuvens
        for nuvem in self.nuvens:
            nuvem.atualizar(velocidade)

        # Ciclo Dia / Noite estilo Dino Run
        self.tempo_ciclo += 1
        periodo = (self.duracao_fase + self.duracao_transicao) * 2
        fase_atual = self.tempo_ciclo % periodo

        if fase_atual < self.duracao_fase:
            # Dia
            self.fator_noite = 0.0
        elif fase_atual < self.duracao_fase + self.duracao_transicao:
            # Transição Dia -> Noite
            p = (fase_atual - self.duracao_fase) / self.duracao_transicao
            self.fator_noite = p
        elif fase_atual < self.duracao_fase * 2 + self.duracao_transicao:
            # Noite
            self.fator_noite = 1.0
        else:
            # Transição Noite -> Dia
            p = (fase_atual - (self.duracao_fase * 2 + self.duracao_transicao)) / self.duracao_transicao
            self.fator_noite = 1.0 - p

    def desenhar(self, tela):
        bg_dia = self.assets.imagens.get("bg_dia")
        bg_noite = self.assets.imagens.get("bg_noite")

        # 1. Desenha o fundo com ciclo espelhado (garante continuidade 100% perfeita)
        if bg_dia and self.bg_dia_flip:
            x1 = int(self.x_fundo)
            # Desenha bloco dia
            tela.blit(bg_dia, (x1, 0))
            tela.blit(self.bg_dia_flip, (x1 + LARGURA, 0))
            tela.blit(self.bg_dia_flip, (x1 - LARGURA, 0))
            tela.blit(bg_dia, (x1 - self.largura_ciclo_bg, 0))

            if bg_noite and self.bg_noite_flip and self.fator_noite > 0.0:
                alpha = int(255 * self.fator_noite)
                bg_noite.set_alpha(alpha)
                self.bg_noite_flip.set_alpha(alpha)
                tela.blit(bg_noite, (x1, 0))
                tela.blit(self.bg_noite_flip, (x1 + LARGURA, 0))
                tela.blit(self.bg_noite_flip, (x1 - LARGURA, 0))
                tela.blit(bg_noite, (x1 - self.largura_ciclo_bg, 0))
                tela.blit(bg_noite, (x1 + LARGURA, 0))
        else:
            # Fallback com gradiente caso imagem não carregue
            cor_ceu = (
                int(AZUL_CEU_DIA[0] * (1 - self.fator_noite) + AZUL_CEU_NOITE[0] * self.fator_noite),
                int(AZUL_CEU_DIA[1] * (1 - self.fator_noite) + AZUL_CEU_NOITE[1] * self.fator_noite),
                int(AZUL_CEU_DIA[2] * (1 - self.fator_noite) + AZUL_CEU_NOITE[2] * self.fator_noite),
            )
            tela.fill(cor_ceu)

        # 2. Estrelas cintilantes na noite
        if self.fator_noite > 0.15:
            alpha_estrelas = int(255 * min(1.0, (self.fator_noite - 0.15) / 0.85))
            for est in self.estrelas:
                brilho_osc = (math.sin(self.tempo_ciclo * 0.08 + est["fase"]) + 1) * 0.5
                alpha_final = int(alpha_estrelas * est["brilho"] * (0.6 + 0.4 * brilho_osc))
                if alpha_final > 10:
                    s = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 255, 255, alpha_final), (2, 2), est["raio"])
                    tela.blit(s, (est["x"], est["y"]))

        # 3. Nuvens suaves
        alpha_nuvem = int(240 * (1.0 - self.fator_noite * 0.6))
        for nuvem in self.nuvens:
            nuvem.desenhar(tela, alpha_nuvem)

        # 4. Chão com rolagem contínua
        x_c = int(self.x_chao)
        tela.blit(self.surf_chao, (x_c, Y_CHAO))
        tela.blit(self.surf_chao, (x_c - LARGURA, Y_CHAO))
        tela.blit(self.surf_chao, (x_c + LARGURA, Y_CHAO))

        # Se for noite, aplica um leve filtro azul escuro sobre o chão para atmosfera
        if self.fator_noite > 0.05:
            sombra_chao = pygame.Surface((LARGURA, ALTURA_CHAO), pygame.SRCALPHA)
            sombra_chao.fill((10, 15, 35, int(110 * self.fator_noite)))
            tela.blit(sombra_chao, (0, Y_CHAO))
