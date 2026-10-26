"""
Entidades do jogo: Obstáculos (Banheira, Shampoo) e Colecionáveis (Petisco, Brinquedo).
"""
import math
import random
import pygame
from src.config import LARGURA, Y_CHAO, PONTOS_PETISCO, PONTOS_BRINQUEDO
from src.asset_manager import AssetManager


class Obstaculo:
    def __init__(self, tipo=None, x_inicial=None):
        self.assets = AssetManager()
        self.tipo = tipo or random.choice(["banheira", "shampoo"])

        if self.tipo == "banheira":
            self.largura = 94
            self.altura = 85
            self.imagem = self.assets.imagens.get("banheira")
        else:
            self.largura = 64
            self.altura = 60
            self.imagem = self.assets.imagens.get("shampoo")

        self.x = float(x_inicial if x_inicial is not None else LARGURA + random.randint(10, 40))
        self.y = Y_CHAO - self.altura

        # Efeito de bolhas saindo do obstáculo
        self.tempo_bolha = random.randint(0, 15)

    def atualizar(self, velocidade, particulas=None):
        self.x -= velocidade

        # Cria bolhinhas de sabão ocasionais
        self.tempo_bolha += 1
        if self.tempo_bolha >= 20 and particulas:
            self.tempo_bolha = 0
            if self.tipo == "banheira":
                particulas.criar_bolhas(self.x + random.randint(15, self.largura - 15), self.y + 15, qtd=1)
            else:
                particulas.criar_bolhas(self.x + self.largura // 2, self.y + 10, qtd=1)

    def desenhar(self, tela):
        if self.imagem:
            tela.blit(self.imagem, (int(self.x), int(self.y)))
        else:
            # Fallback
            cor = (70, 150, 220) if self.tipo == "banheira" else (50, 200, 180)
            pygame.draw.rect(tela, cor, (int(self.x), int(self.y), self.largura, self.altura))

    def hitbox(self):
        """Hitbox justa para cada tipo de obstáculo."""
        if self.tipo == "banheira":
            return pygame.Rect(
                int(self.x + 8),
                int(self.y + 18),
                self.largura - 16,
                self.altura - 18
            )
        # Shampoo
        return pygame.Rect(
            int(self.x + 10),
            int(self.y + 10),
            self.largura - 20,
            self.altura - 10
        )

    def saiu_da_tela(self):
        return self.x + self.largura < -40


class Colecionavel:
    def __init__(self, tipo=None, x_inicial=None, altura_pulo=None):
        self.assets = AssetManager()
        self.tipo = tipo or random.choice(["petisco", "brinquedo"])

        if self.tipo == "petisco":
            self.largura = 50
            self.altura = 46
            self.valor = PONTOS_PETISCO
            self.imagem = self.assets.imagens.get("petisco")
            self.cor_texto = (255, 220, 50)
        else:
            self.largura = 46
            self.altura = 54
            self.valor = PONTOS_BRINQUEDO
            self.imagem = self.assets.imagens.get("brinquedo")
            self.cor_texto = (255, 110, 40)

        self.x = float(x_inicial if x_inicial is not None else LARGURA + random.randint(15, 60))

        # Altura: chão, salto médio ou salto alto
        if altura_pulo is not None:
            self.altura_chao_offset = altura_pulo
        else:
            self.altura_chao_offset = random.choice([18, 75, 115])

        self.base_y = Y_CHAO - self.altura - self.altura_chao_offset
        self.y = self.base_y
        self.tempo_flutuacao = random.uniform(0, math.pi * 2)

    def atualizar(self, velocidade, particulas=None):
        self.x -= velocidade
        self.tempo_flutuacao += 0.08
        # Flutuação senoidal graciosa
        self.y = self.base_y + math.sin(self.tempo_flutuacao) * 5.5

        # Brilho sutil periódico
        if particulas and random.random() < 0.04:
            particulas.criar_brilhos(self.x + self.largura // 2, self.y + self.altura // 2, qtd=1, cor=self.cor_texto)

    def desenhar(self, tela):
        # Leve halo brilhante atrás do item
        halo_raio = max(self.largura, self.altura) // 2 + 5
        halo_surf = pygame.Surface((halo_raio * 2, halo_raio * 2), pygame.SRCALPHA)
        cor_halo = (*self.cor_texto, 40)
        pygame.draw.circle(halo_surf, cor_halo, (halo_raio, halo_raio), halo_raio)
        tela.blit(halo_surf, (int(self.x + self.largura // 2 - halo_raio), int(self.y + self.altura // 2 - halo_raio)))

        if self.imagem:
            tela.blit(self.imagem, (int(self.x), int(self.y)))
        else:
            pygame.draw.circle(tela, self.cor_texto, (int(self.x + self.largura // 2), int(self.y + self.altura // 2)), 20)

    def hitbox(self):
        return pygame.Rect(
            int(self.x + 6),
            int(self.y + 6),
            self.largura - 12,
            self.altura - 12
        )

    def saiu_da_tela(self):
        return self.x + self.largura < -40
