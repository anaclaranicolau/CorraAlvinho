"""
Controlador central do jogo Corra, Alvinho!
Gerencia máquina de estados, spawn inteligente, loop principal e persistência de recorde.
"""
import json
import os
import random
import pygame
from src.config import (
    LARGURA, ALTURA, TITULO, FPS,
    VELOCIDADE_INICIAL, VELOCIDADE_MAXIMA, ACELERACAO_VELOCIDADE,
    ARQUIVO_HIGHSCORE, INTERVALO_MILESTONE
)
from src.asset_manager import AssetManager
from src.particles import GerenciadorParticulas
from src.background import CenarioParalaxe
from src.alvinho import Alvinho
from src.entities import Obstaculo, Colecionavel
from src.ui import UI


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()

        self.assets = AssetManager()
        self.particulas = GerenciadorParticulas()
        self.cenario = CenarioParalaxe()
        self.alvinho = Alvinho(self.particulas)
        self.ui = UI()

        # Recorde salvo
        self.recorde = self.carregar_recorde()
        self.novo_recorde = False

        # Estado do jogo: "MENU", "JOGANDO", "GAME_OVER"
        self.estado = "MENU"
        self.executando = True

        # Variáveis da partida
        self.velocidade = VELOCIDADE_INICIAL
        self.pontuacao = 0
        self.distancia_acumulada = 0.0
        self.ultimo_milestone = 0
        self.timer_flash_milestone = 0

        self.petiscos_coletados = 0
        self.brinquedos_coletados = 0

        self.obstaculos = []
        self.colecionaveis = []

        # Controle de espaçamento (estilo Dino Run)
        self.dist_ultimo_obstaculo = 0.0
        self.proximo_obstaculo_dist = 350.0

        self.dist_ultimo_item = 0.0
        self.proximo_item_dist = 420.0

        # Efeito de tremor de tela (screen shake) no impacto
        self.tremer_tela = 0

        # Delay anti-clique acidental na derrota
        self.cooldown_game_over = 0

        # Inicia a música de fundo
        self.assets.tocar_musica()

    def carregar_recorde(self):
        if os.path.exists(ARQUIVO_HIGHSCORE):
            try:
                with open(ARQUIVO_HIGHSCORE, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    return int(dados.get("recorde", 0))
            except Exception:
                pass
        return 0

    def salvar_recorde(self):
        try:
            with open(ARQUIVO_HIGHSCORE, "w", encoding="utf-8") as f:
                json.dump({"recorde": self.recorde}, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar recorde: {e}")

    def iniciar_partida(self):
        self.alvinho.reiniciar()
        self.particulas.limpar()
        self.obstaculos.clear()
        self.colecionaveis.clear()

        self.velocidade = VELOCIDADE_INICIAL
        self.pontuacao = 0
        self.distancia_acumulada = 0.0
        self.ultimo_milestone = 0
        self.timer_flash_milestone = 0

        self.petiscos_coletados = 0
        self.brinquedos_coletados = 0
        self.novo_recorde = False

        self.dist_ultimo_obstaculo = 0.0
        self.proximo_obstaculo_dist = 360.0

        self.dist_ultimo_item = 0.0
        self.proximo_item_dist = 400.0

        self.tremer_tela = 0
        self.estado = "JOGANDO"

    def processar_interacao_unica_down(self):
        """O ÚNICO botão de interação do jogo (Barra de Espaço)."""
        if self.estado == "MENU":
            self.iniciar_partida()
            self.alvinho.solicitar_pulo()

        elif self.estado == "JOGANDO":
            self.alvinho.solicitar_pulo()

        elif self.estado == "GAME_OVER":
            if self.cooldown_game_over <= 0:
                self.iniciar_partida()
                self.alvinho.solicitar_pulo()

    def processar_interacao_unica_up(self):
        """Soltura do botão de interação para pulo variável."""
        if self.estado == "JOGANDO":
            self.alvinho.soltar_pulo()

    def gerenciar_spawn(self):
        self.dist_ultimo_obstaculo += self.velocidade
        self.dist_ultimo_item += self.velocidade

        # 1. Spawn de Obstáculos (garantindo ritmo justo do Dino Run)
        if self.dist_ultimo_obstaculo >= self.proximo_obstaculo_dist:
            # Chance de cluster de 2 shampoos próximos quando a velocidade for maior
            if self.velocidade > 10.0 and random.random() < 0.28:
                # Combo: 2 shampoos
                self.obstaculos.append(Obstaculo(tipo="shampoo", x_inicial=LARGURA + 20))
                self.obstaculos.append(Obstaculo(tipo="shampoo", x_inicial=LARGURA + 85))
            else:
                tipo = "banheira" if random.random() < 0.52 else "shampoo"
                self.obstaculos.append(Obstaculo(tipo=tipo))

            self.dist_ultimo_obstaculo = 0.0
            # Distância mínima e máxima baseada na velocidade atual
            min_dist = int(290 + self.velocidade * 14)
            max_dist = int(480 + self.velocidade * 22)
            self.proximo_obstaculo_dist = random.randint(min_dist, max_dist)

        # 2. Spawn de Colecionáveis
        if self.dist_ultimo_item >= self.proximo_item_dist:
            # Só cria se não estiver em cima de um obstáculo recém criado
            if self.dist_ultimo_obstaculo > 120 and (self.proximo_obstaculo_dist - self.dist_ultimo_obstaculo) > 130:
                tipo_item = "brinquedo" if random.random() < 0.35 else "petisco"
                self.colecionaveis.append(Colecionavel(tipo=tipo_item))
                self.dist_ultimo_item = 0.0
                self.proximo_item_dist = random.randint(260, 480)

    def atualizar_partida(self):
        # Aceleração progressiva do jogo
        if self.velocidade < VELOCIDADE_MAXIMA:
            self.velocidade += ACELERACAO_VELOCIDADE

        # Pontuação baseada em distância (estilo Dino Run)
        self.distancia_acumulada += self.velocidade * 0.12
        if self.distancia_acumulada >= 1.0:
            pontos_dist = int(self.distancia_acumulada)
            self.pontuacao += pontos_dist
            self.distancia_acumulada -= pontos_dist

        # Checa novo recorde durante o gameplay
        if self.pontuacao > self.recorde:
            self.recorde = self.pontuacao
            self.novo_recorde = True

        # Efeito de Milestone a cada 100 pontos
        if self.pontuacao // INTERVALO_MILESTONE > self.ultimo_milestone:
            self.ultimo_milestone = self.pontuacao // INTERVALO_MILESTONE
            self.timer_flash_milestone = 35
            self.assets.tocar_milestone()

        if self.timer_flash_milestone > 0:
            self.timer_flash_milestone -= 1

        # Atualiza cenário, jogador e partículas
        self.cenario.atualizar(self.velocidade)
        self.alvinho.atualizar(self.velocidade)
        self.particulas.atualizar()

        # Gera novos obstáculos e colecionáveis
        self.gerenciar_spawn()

        hitbox_alvinho = self.alvinho.hitbox()

        # Atualiza obstáculos e checa colisão
        for obs in self.obstaculos:
            obs.atualizar(self.velocidade, self.particulas)
            if hitbox_alvinho.colliderect(obs.hitbox()):
                # Colisão com banho! Fim de jogo!
                self.alvinho.tomar_dano()
                self.tremer_tela = 14
                self.cooldown_game_over = 22  # frames de espera
                self.estado = "GAME_OVER"
                if self.novo_recorde:
                    self.salvar_recorde()
                # Cria explosão de bolhas de sabão no impacto
                self.particulas.criar_bolhas(self.alvinho.x + 40, self.alvinho.y + 30, qtd=12)
                break

        # Remove obstáculos fora da tela
        self.obstaculos = [obs for obs in self.obstaculos if not obs.saiu_da_tela()]

        # Atualiza colecionáveis e checa coleta
        for item in self.colecionaveis[:]:
            item.atualizar(self.velocidade, self.particulas)
            if hitbox_alvinho.colliderect(item.hitbox()):
                # Coletou o item! Toca áudio de latido conforme solicitado
                self.assets.tocar_latido()

                # Pontuação e contagem
                self.pontuacao += item.valor
                if item.tipo == "petisco":
                    self.petiscos_coletados += 1
                else:
                    self.brinquedos_coletados += 1

                # Efeitos visuais de estrelas e texto flutuante
                self.particulas.criar_brilhos(
                    item.x + item.largura // 2,
                    item.y + item.altura // 2,
                    qtd=14,
                    cor=item.cor_texto
                )
                self.particulas.criar_texto_pontos(
                    f"+{item.valor}",
                    item.x + item.largura // 2,
                    item.y - 8,
                    item.cor_texto,
                    self.assets.fontes.get("media")
                )

                self.colecionaveis.remove(item)

        # Remove itens fora da tela
        self.colecionaveis = [item for item in self.colecionaveis if not item.saiu_da_tela()]

    def loop_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False

            # Pressionou tecla
            elif evento.type == pygame.KEYDOWN:
                # O ÚNICO BOTÃO DE INTERAÇÃO (apenas a Barra de Espaço)
                if evento.key == pygame.K_SPACE:
                    self.processar_interacao_unica_down()

                # Atalho opcional para mutar áudio
                elif evento.key == pygame.K_m:
                    self.assets.alternar_som()

            # Soltou tecla (para salto de altura variável)
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    self.processar_interacao_unica_up()

    def desenhar(self):
        # Deslocamento de tremor de tela (screen shake)
        offset_x, offset_y = 0, 0
        if self.tremer_tela > 0:
            self.tremer_tela -= 1
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-3, 3)

        # Desenha em uma superfície intermediária para aplicar o screen shake com perfeição
        superficie_jogo = pygame.Surface((LARGURA, ALTURA))

        # 1. Desenha o Cenário (céu, nuvens, dia/noite e chão)
        self.cenario.desenhar(superficie_jogo)

        # 2. Desenha Colecionáveis
        for item in self.colecionaveis:
            item.desenhar(superficie_jogo)

        # 3. Desenha Obstáculos
        for obs in self.obstaculos:
            obs.desenhar(superficie_jogo)

        # 4. Desenha Alvinho
        self.alvinho.desenhar(superficie_jogo)

        # 5. Desenha Partículas e Textos Flutuantes
        self.particulas.desenhar(superficie_jogo)

        # 6. Desenha HUD ou Menus
        if self.estado == "JOGANDO":
            piscar = (self.timer_flash_milestone // 6) % 2 == 1
            self.ui.desenhar_hud(
                superficie_jogo,
                self.pontuacao,
                self.recorde,
                self.petiscos_coletados,
                self.brinquedos_coletados,
                piscar_milestone=piscar
            )
        elif self.estado == "MENU":
            self.ui.desenhar_menu_inicio(superficie_jogo, self.recorde)
        elif self.estado == "GAME_OVER":
            self.ui.desenhar_game_over(
                superficie_jogo,
                self.pontuacao,
                self.recorde,
                self.novo_recorde,
                self.petiscos_coletados,
                self.brinquedos_coletados
            )

        # Blita com screen shake na tela real
        self.tela.blit(superficie_jogo, (offset_x, offset_y))
        pygame.display.flip()

    def executar(self):
        while self.executando:
            self.relogio.tick(FPS)
            self.loop_eventos()
            self.ui.atualizar()

            if self.estado == "JOGANDO":
                self.atualizar_partida()
            elif self.estado == "GAME_OVER":
                if self.cooldown_game_over > 0:
                    self.cooldown_game_over -= 1
                self.alvinho.atualizar(0)
                self.particulas.atualizar()

            self.desenhar()

        # Salva o recorde ao fechar
        self.salvar_recorde()
        pygame.quit()
