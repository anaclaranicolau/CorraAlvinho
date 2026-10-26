"""
Classe do protagonista Alvinho.
Controla física, estados de pulo responsivo (estilo Chrome Dino), animações e colisões.
"""
import pygame
from src.config import Y_CHAO, GRAVIDADE, GRAVIDADE_PULO_ALTO, FORCA_PULO
from src.asset_manager import AssetManager


class Alvinho:
    def __init__(self, gerenciador_particulas=None):
        self.assets = AssetManager()
        self.particulas = gerenciador_particulas

        # Dimensões e posição
        self.largura = 96
        self.altura = 79
        self.x = 110
        self.y = Y_CHAO - self.altura

        # Física do pulo (estilo Dino Run / Mario)
        self.velocidade_y = 0.0
        self.no_chao = True
        self.segurando_pulo = False
        self.buffer_pulo = 0    # Frames para registrar pulo antecipado
        self.coyote_time = 0    # Frames de tolerância ao sair do chão
        self.derrotado = False

        # Controle de Animação
        self.frame_atual = 0
        self.tempo_animacao = 0
        self.contador_passo = 0

        # Rotação para dinâmica de salto
        self.angulo_rotacao = 0.0

        # Efeito de impacto quando derrotado
        self.tempo_derrota = 0
        self.y_derrota_offset = 0

    def reiniciar(self):
        self.y = Y_CHAO - self.altura
        self.velocidade_y = 0.0
        self.no_chao = True
        self.segurando_pulo = False
        self.buffer_pulo = 0
        self.coyote_time = 0
        self.derrotado = False
        self.frame_atual = 0
        self.tempo_animacao = 0
        self.angulo_rotacao = 0.0
        self.tempo_derrota = 0
        self.y_derrota_offset = 0

    def solicitar_pulo(self):
        """Chamado quando o único botão de interação é pressionado."""
        if self.derrotado:
            return

        self.segurando_pulo = True

        if self.no_chao or self.coyote_time > 0:
            self._executar_pulo()
        else:
            # Pressionou no ar: guarda no buffer por até 7 frames
            self.buffer_pulo = 7

    def soltar_pulo(self):
        """Chamado quando o botão de interação é solto (para pulo de altura variável)."""
        self.segurando_pulo = False

    def _executar_pulo(self):
        self.velocidade_y = FORCA_PULO
        self.no_chao = False
        self.coyote_time = 0
        self.buffer_pulo = 0
        self.assets.tocar_pulo()

        # Cria nuvem de poeira no impulso
        if self.particulas:
            self.particulas.criar_poeira(self.x + 25, Y_CHAO - 2, qtd=5)

    def tomar_dano(self):
        if not self.derrotado:
            self.derrotado = True
            self.velocidade_y = -6.5  # pequeno pulinho de susto
            self.no_chao = False
            self.assets.tocar_derrota()

    def atualizar(self, vel_jogo=7.0):
        # Se estiver derrotado, faz uma animaçãozinha de tropeço
        if self.derrotado:
            self.tempo_derrota += 1
            if not self.no_chao:
                self.velocidade_y += GRAVIDADE
                self.y += self.velocidade_y
                if self.y >= Y_CHAO - self.altura:
                    self.y = Y_CHAO - self.altura
                    self.velocidade_y = 0
                    self.no_chao = True
            return

        # Decrementa timers de buffer e coyote
        if self.buffer_pulo > 0:
            self.buffer_pulo -= 1

        if not self.no_chao and self.coyote_time > 0:
            self.coyote_time -= 1

        # Aplica gravidade variável:
        # Se estiver subindo e segurando o botão, gravidade mais leve para salto mais alto
        if self.velocidade_y < 0 and self.segurando_pulo:
            self.velocidade_y += GRAVIDADE_PULO_ALTO
        else:
            self.velocidade_y += GRAVIDADE

        self.y += self.velocidade_y

        # Colisão com o chão
        if self.y >= Y_CHAO - self.altura:
            era_no_ar = not self.no_chao
            self.y = Y_CHAO - self.altura
            self.velocidade_y = 0
            self.no_chao = True
            self.coyote_time = 5

            # Se acabou de aterrissar
            if era_no_ar and self.particulas:
                self.particulas.criar_poeira(self.x + 35, Y_CHAO - 2, qtd=4)

            # Se havia um pulo armazenado no buffer, pula imediatamente
            if self.buffer_pulo > 0:
                self._executar_pulo()

        # Atualiza animação
        if self.no_chao:
            # Velocidade de animação das patinhas acelera conforme a velocidade do jogo
            limite_tempo = max(4, int(9 - (vel_jogo - 6.5) * 0.4))
            self.tempo_animacao += 1
            if self.tempo_animacao >= limite_tempo:
                self.frame_atual = 1 - self.frame_atual
                self.tempo_animacao = 0

            # Poeirinha contínua das patinhas correndo
            self.contador_passo += 1
            if self.contador_passo >= 10:
                self.contador_passo = 0
                if self.particulas:
                    self.particulas.criar_poeira(self.x + 15, Y_CHAO - 4, qtd=1)

            self.angulo_rotacao = 0.0
        else:
            # No ar: inclina ligeiramente para cima subindo e para baixo caindo
            if self.velocidade_y < -2:
                self.angulo_rotacao = min(12.0, self.angulo_rotacao + 2.0)
            elif self.velocidade_y > 2:
                self.angulo_rotacao = max(-10.0, self.angulo_rotacao - 1.8)
            else:
                self.angulo_rotacao *= 0.8

    def desenhar(self, tela):
        if self.derrotado:
            img = self.assets.imagens.get("alvinho_hurt")
            if img:
                # Pequena vibração cômica quando parado derrotado
                offset_x = 0
                if self.tempo_derrota < 20 and self.tempo_derrota % 4 < 2:
                    offset_x = 2
                tela.blit(img, (self.x + offset_x, self.y))
            return

        if not self.no_chao:
            img = self.assets.imagens.get("alvinho_jump")
            if img:
                # Ajusta para os pés tocarem a mesma altura base
                desenho_y = self.y - 12
                if abs(self.angulo_rotacao) > 1:
                    img_rot = pygame.transform.rotate(img, self.angulo_rotacao)
                    rect = img_rot.get_rect(center=(self.x + self.largura // 2, int(desenho_y + 45)))
                    tela.blit(img_rot, rect)
                else:
                    tela.blit(img, (self.x, int(desenho_y)))
            return

        # No chão correndo
        chave_frame = "alvinho_run0" if self.frame_atual == 0 else "alvinho_run1"
        img = self.assets.imagens.get(chave_frame)
        if img:
            tela.blit(img, (self.x, int(self.y)))

    def hitbox(self):
        """Hitbox justa e precisa para não frustrar o jogador com bordas de pelo."""
        if not self.no_chao:
            # No ar: ligeiramente mais compacto
            return pygame.Rect(
                self.x + 18,
                self.y + 12,
                self.largura - 32,
                self.altura - 22
            )
        return pygame.Rect(
            self.x + 16,
            self.y + 14,
            self.largura - 28,
            self.altura - 18
        )
