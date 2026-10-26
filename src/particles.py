"""
Sistema de partículas e efeitos visuais do jogo.
Poeira das patas, brilhos de coleta, bolhas de sabão e textos flutuantes de pontuação.
"""
import random
import math
import pygame


class ParticulaPoeira:
    def __init__(self, x, y):
        self.x = x + random.uniform(-4, 4)
        self.y = y + random.uniform(-2, 3)
        self.vx = random.uniform(-2.8, -1.0)
        self.vy = random.uniform(-1.8, -0.4)
        self.tamanho = random.uniform(3.5, 7.0)
        self.vida = random.randint(18, 30)
        self.vida_max = self.vida
        # Tons de terra/grama suave
        self.cor = random.choice([
            (215, 205, 185),
            (190, 180, 160),
            (170, 160, 140),
            (145, 195, 130)  # toques de graminha
        ])

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # gravidade leve
        self.vida -= 1
        self.tamanho = max(0.5, self.tamanho * 0.94)

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha = int(255 * (self.vida / self.vida_max))
        raio = int(self.tamanho)
        if raio < 1:
            return
        surf = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.cor, alpha), (raio, raio), raio)
        tela.blit(surf, (int(self.x - raio), int(self.y - raio)))


class ParticulaBrilho:
    def __init__(self, x, y, cor=None):
        self.x = x
        self.y = y
        angulo = random.uniform(0, math.pi * 2)
        velocidade = random.uniform(2.0, 5.5)
        self.vx = math.cos(angulo) * velocidade
        self.vy = math.sin(angulo) * velocidade
        self.tamanho = random.uniform(3.0, 6.0)
        self.vida = random.randint(22, 36)
        self.vida_max = self.vida
        self.cor = cor or random.choice([
            (255, 235, 100),
            (255, 215, 0),
            (255, 255, 255),
            (255, 170, 50)
        ])

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha = int(255 * (self.vida / self.vida_max))
        t = int(self.tamanho * (self.vida / self.vida_max))
        if t < 1:
            return
        surf = pygame.Surface((t * 2 + 2, t * 2 + 2), pygame.SRCALPHA)
        # Desenha uma estrelinha com cruz e centro
        cx, cy = t + 1, t + 1
        cor_com_alpha = (*self.cor, alpha)
        pygame.draw.line(surf, cor_com_alpha, (cx - t, cy), (cx + t, cy), 2)
        pygame.draw.line(surf, cor_com_alpha, (cx, cy - t), (cx, cy + t), 2)
        pygame.draw.circle(surf, (255, 255, 255, alpha), (cx, cy), max(1, t // 2))
        tela.blit(surf, (int(self.x - cx), int(self.y - cy)))


class ParticulaBolha:
    def __init__(self, x, y):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-6, 6)
        self.vx = random.uniform(-1.2, 0.4)
        self.vy = random.uniform(-1.5, -0.6)
        self.tamanho = random.uniform(4.0, 9.0)
        self.vida = random.randint(30, 55)
        self.vida_max = self.vida
        self.oscilacao = random.uniform(0, math.pi * 2)

    def atualizar(self):
        self.oscilacao += 0.1
        self.x += self.vx + math.sin(self.oscilacao) * 0.4
        self.y += self.vy
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha = int(210 * (self.vida / self.vida_max))
        raio = int(self.tamanho)
        if raio < 2:
            return
        surf = pygame.Surface((raio * 2 + 2, raio * 2 + 2), pygame.SRCALPHA)
        cx, cy = raio + 1, raio + 1
        # Borda iridescente suave
        pygame.draw.circle(surf, (160, 225, 255, alpha), (cx, cy), raio, 2)
        # Brilho de reflexo na bolha
        brilho_raio = max(1, raio // 3)
        pygame.draw.circle(surf, (255, 255, 255, int(alpha * 0.8)), (cx - raio // 3, cy - raio // 3), brilho_raio)
        tela.blit(surf, (int(self.x - cx), int(self.y - cy)))


class TextoFlutuante:
    def __init__(self, texto, x, y, cor, fonte):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.fonte = fonte
        self.vida = 45
        self.vida_max = 45
        self.vy = -1.8

    def atualizar(self):
        self.y += self.vy
        self.vy *= 0.94
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida <= 0:
            return
        alpha = int(255 * (self.vida / self.vida_max))
        surf_texto = self.fonte.render(self.texto, True, self.cor)
        surf = pygame.Surface(surf_texto.get_size(), pygame.SRCALPHA)
        surf.blit(surf_texto, (0, 0))
        surf.set_alpha(alpha)
        # Contorno escuro para contraste
        surf_sombra = self.fonte.render(self.texto, True, (20, 20, 20))
        sombra = pygame.Surface(surf_sombra.get_size(), pygame.SRCALPHA)
        sombra.blit(surf_sombra, (0, 0))
        sombra.set_alpha(int(alpha * 0.7))

        rect = surf.get_rect(center=(int(self.x), int(self.y)))
        tela.blit(sombra, (rect.x + 1, rect.y + 1))
        tela.blit(surf, rect)


class GerenciadorParticulas:
    def __init__(self):
        self.particulas = []
        self.textos = []

    def criar_poeira(self, x, y, qtd=2):
        for _ in range(qtd):
            self.particulas.append(ParticulaPoeira(x, y))

    def criar_brilhos(self, x, y, qtd=12, cor=None):
        for _ in range(qtd):
            self.particulas.append(ParticulaBrilho(x, y, cor))

    def criar_bolhas(self, x, y, qtd=3):
        for _ in range(qtd):
            self.particulas.append(ParticulaBolha(x, y))

    def criar_texto_pontos(self, texto, x, y, cor, fonte):
        self.textos.append(TextoFlutuante(texto, x, y, cor, fonte))

    def atualizar(self):
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.vida > 0]

        for t in self.textos:
            t.atualizar()
        self.textos = [t for t in self.textos if t.vida > 0]

    def desenhar(self, tela):
        for p in self.particulas:
            p.desenhar(tela)
        for t in self.textos:
            t.desenhar(tela)

    def limpar(self):
        self.particulas.clear(
        )
        self.textos.clear()
