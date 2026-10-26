"""
Interfaces visuais, menus estilizados, HUD e tela de Game Over.
Totalmente navegável com apenas a Barra de Espaço.
"""
import math
import pygame
from src.config import LARGURA, ALTURA, BRANCO, PRETO, AMARELO_OURO, LARANJA, VERMELHO_CORACAO
from src.asset_manager import AssetManager


class UI:
    def __init__(self):
        self.assets = AssetManager()
        self.tempo_pulso = 0

    def atualizar(self):
        self.tempo_pulso += 0.06

    def desenhar_hud(self, tela, pontuacao, recorde, petiscos, brinquedos, piscar_milestone=False):
        # 1. Pontuação estilo Chrome Dino no canto superior direito
        str_score = f"{pontuacao:05d}"
        str_hi = f"HI {recorde:05d}"

        cor_texto = (255, 255, 255)
        if piscar_milestone:
            # Efeito de piscar do Dino Run
            cor_texto = AMARELO_OURO

        fonte_dig = self.assets.fontes.get("digital", pygame.font.Font(None, 24))

        # Placa de fundo para o HUD com cantos arredondados e transparência
        hud_bg = pygame.Surface((230, 42), pygame.SRCALPHA)
        hud_bg.fill((20, 25, 35, 175))
        pygame.draw.rect(hud_bg, (255, 255, 255, 40), (0, 0, 230, 42), 1, border_radius=8)
        tela.blit(hud_bg, (LARGURA - 245, 15))

        # Texto HI e Score atual
        txt_hi = fonte_dig.render(str_hi, True, (180, 190, 205))
        txt_sc = fonte_dig.render(str_score, True, cor_texto)
        tela.blit(txt_hi, (LARGURA - 235, 24))
        tela.blit(txt_sc, (LARGURA - 120, 24))

        # 2. Contador de itens coletados no canto superior esquerdo
        col_bg = pygame.Surface((210, 42), pygame.SRCALPHA)
        col_bg.fill((20, 25, 35, 175))
        pygame.draw.rect(col_bg, (255, 255, 255, 40), (0, 0, 210, 42), 1, border_radius=8)
        tela.blit(col_bg, (18, 15))

        # Mini ícone do petisco
        img_petisco = self.assets.imagens.get("petisco")
        if img_petisco:
            mini_p = pygame.transform.smoothscale(img_petisco, (24, 22))
            tela.blit(mini_p, (26, 25))
        txt_p = fonte_dig.render(f"x{petiscos}", True, AMARELO_OURO)
        tela.blit(txt_p, (55, 25))

        # Mini ícone do brinquedo
        img_brinquedo = self.assets.imagens.get("brinquedo")
        if img_brinquedo:
            mini_b = pygame.transform.smoothscale(img_brinquedo, (20, 24))
            tela.blit(mini_b, (120, 24))
        txt_b = fonte_dig.render(f"x{brinquedos}", True, LARANJA)
        tela.blit(txt_b, (148, 25))

    def desenhar_menu_inicio(self, tela, recorde):
        # Painel central moderno
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((15, 20, 35, 150))
        tela.blit(overlay, (0, 0))

        # Cartão central de vidro (Glassmorphism)
        card_w, card_h = 680, 390
        card_x = (LARGURA - card_w) // 2
        card_y = (ALTURA - card_h) // 2
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card_surf.fill((25, 32, 50, 215))
        pygame.draw.rect(card_surf, (255, 255, 255, 60), (0, 0, card_w, card_h), 2, border_radius=20)
        tela.blit(card_surf, (card_x, card_y))

        # Título vibrante com sombra
        fonte_tit = self.assets.fontes.get("titulo")
        fonte_sub = self.assets.fontes.get("subtitulo")
        fonte_med = self.assets.fontes.get("media")
        fonte_norm = self.assets.fontes.get("normal")
        fonte_peq = self.assets.fontes.get("pequena")

        # Flutuação sutil do título
        offset_y = math.sin(self.tempo_pulso * 1.5) * 4

        # Sombra do título
        tit_sombra = fonte_tit.render("CORRA, ALVINHO!", True, (10, 15, 25))
        tit_surf = fonte_tit.render("CORRA, ALVINHO!", True, AMARELO_OURO)
        tela.blit(tit_sombra, (LARGURA // 2 - tit_sombra.get_width() // 2 + 2, card_y + 25 + int(offset_y) + 2))
        tela.blit(tit_surf, (LARGURA // 2 - tit_surf.get_width() // 2, card_y + 25 + int(offset_y)))

        # Subtítulo
        sub_surf = fonte_sub.render("Fugindo da Hora do Banho!", True, BRANCO)
        tela.blit(sub_surf, (LARGURA // 2 - sub_surf.get_width() // 2, card_y + 95))

        # Mini prévia do Alvinho com círculo de destaque
        pedestal_x = card_x + 95
        pedestal_y = card_y + 200
        pedestal_surf = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(pedestal_surf, (255, 255, 255, 25), (60, 60), 55)
        pygame.draw.circle(pedestal_surf, (255, 215, 0, 50), (60, 60), 55, 2)
        tela.blit(pedestal_surf, (pedestal_x - 60, pedestal_y - 60))

        img_alvinho = self.assets.imagens.get("alvinho_run0")
        if img_alvinho:
            tela.blit(img_alvinho, (pedestal_x - img_alvinho.get_width() // 2, pedestal_y - img_alvinho.get_height() // 2))

        # Caixa explicativa dos controles e regras
        info_x = card_x + 175
        info_y = card_y + 140

        linhas_instrucoes = [
            ("COMANDO UNICO:", AMARELO_OURO, True),
            ("• Pressione ESPACO para PULAR", BRANCO, False),
            ("• Segure ESPACO para dar um salto mais alto!", (200, 230, 255), False),
            ("• Pule sobre as Banheiras e Shampoos de espuma!", (255, 175, 175), False),
            ("• Pegue Petiscos e Brinquedos com latidos felizes!", (175, 255, 175), False),
        ]

        for texto, cor, eh_destaque in linhas_instrucoes:
            f = fonte_med if eh_destaque else fonte_norm
            s = f.render(texto, True, cor)
            tela.blit(s, (info_x, info_y))
            info_y += 24 if eh_destaque else 21

        # Recorde salvo
        txt_rec = fonte_med.render(f"[ RECORDE ATUAL: {recorde:05d} ]", True, AMARELO_OURO)
        tela.blit(txt_rec, (LARGURA // 2 - txt_rec.get_width() // 2, card_y + 275))

        # Botão pulsar de ação única com largura ideal
        pulso = (math.sin(self.tempo_pulso * 3.5) + 1) * 0.5
        btn_w, btn_h = 560, 50
        btn_x = (LARGURA - btn_w) // 2
        btn_y = card_y + 318

        cor_btn = (
            int(255 * (0.85 + 0.15 * pulso)),
            int(185 * (0.85 + 0.15 * pulso)),
            int(35 * (0.85 + 0.15 * pulso))
        )
        pygame.draw.rect(tela, cor_btn, (btn_x, btn_y, btn_w, btn_h), border_radius=14)
        pygame.draw.rect(tela, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=14)

        prompt_surf = fonte_med.render("PRESSIONE ESPACO PARA JOGAR", True, PRETO)
        tela.blit(prompt_surf, (btn_x + (btn_w - prompt_surf.get_width()) // 2, btn_y + 13))

    def desenhar_game_over(self, tela, pontuacao, recorde, novo_recorde, petiscos, brinquedos):
        # Escurece com vinheta suave
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((20, 10, 15, 185))
        tela.blit(overlay, (0, 0))

        card_w, card_h = 640, 390
        card_x = (LARGURA - card_w) // 2
        card_y = (ALTURA - card_h) // 2

        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card_surf.fill((30, 25, 40, 235))
        borda_cor = AMARELO_OURO if novo_recorde else (220, 80, 80)
        pygame.draw.rect(card_surf, borda_cor, (0, 0, card_w, card_h), 3, border_radius=20)
        tela.blit(card_surf, (card_x, card_y))

        fonte_tit = self.assets.fontes.get("titulo")
        fonte_sub = self.assets.fontes.get("subtitulo")
        fonte_med = self.assets.fontes.get("media")
        fonte_norm = self.assets.fontes.get("normal")
        fonte_dig = self.assets.fontes.get("digital_grande")

        # Título de Fim de Jogo
        tit_surf = fonte_tit.render("HORA DO BANHO!", True, VERMELHO_CORACAO)
        tela.blit(tit_surf, (LARGURA // 2 - tit_surf.get_width() // 2, card_y + 20))

        sub_surf = fonte_norm.render("Alvinho nao conseguiu fugir da espuma!", True, (215, 215, 225))
        tela.blit(sub_surf, (LARGURA // 2 - sub_surf.get_width() // 2, card_y + 82))

        # Alvinho tonto com pedestal
        pedestal_x = card_x + 95
        pedestal_y = card_y + 195
        pedestal_surf = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(pedestal_surf, (255, 255, 255, 20), (60, 60), 55)
        pygame.draw.circle(pedestal_surf, (220, 80, 80, 60), (60, 60), 55, 2)
        tela.blit(pedestal_surf, (pedestal_x - 60, pedestal_y - 60))

        img_tonto = self.assets.imagens.get("alvinho_hurt")
        if img_tonto:
            tela.blit(img_tonto, (pedestal_x - img_tonto.get_width() // 2, pedestal_y - img_tonto.get_height() // 2))

        # Informações da partida
        info_x = card_x + 180
        info_y = card_y + 125

        txt_pts = fonte_med.render("Pontuacao Final:", True, BRANCO)
        val_pts = fonte_dig.render(f"{pontuacao:05d}", True, AMARELO_OURO)
        tela.blit(txt_pts, (info_x, info_y))
        tela.blit(val_pts, (info_x + 205, info_y - 4))

        info_y += 38
        if novo_recorde:
            # Badge chamativo de Novo Recorde
            pulso = (math.sin(self.tempo_pulso * 4.0) + 1) * 0.5
            cor_rec = (255, int(215 + 40 * pulso), int(50 * pulso))
            txt_novo = fonte_sub.render("NOVO RECORDE PESSOAL!", True, cor_rec)
            tela.blit(txt_novo, (info_x, info_y))
        else:
            txt_rec = fonte_norm.render(f"Melhor Recorde: {recorde:05d}", True, (180, 190, 205))
            tela.blit(txt_rec, (info_x, info_y))

        info_y += 34
        # Estatísticas de colecionáveis
        txt_itens = fonte_norm.render(
            f"Petiscos: {petiscos}  |  Brinquedos: {brinquedos}",
            True,
            (210, 220, 240)
        )
        tela.blit(txt_itens, (info_x, info_y))

        # Botão pulsar de jogar novamente
        pulso = (math.sin(self.tempo_pulso * 3.5) + 1) * 0.5
        btn_w, btn_h = 560, 50
        btn_x = (LARGURA - btn_w) // 2
        btn_y = card_y + 318

        cor_btn = (
            int(50 + 25 * pulso),
            int(185 + 35 * pulso),
            int(95 + 25 * pulso)
        )
        pygame.draw.rect(tela, cor_btn, (btn_x, btn_y, btn_w, btn_h), border_radius=14)
        pygame.draw.rect(tela, (255, 255, 255), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=14)

        prompt_surf = fonte_med.render("PRESSIONE ESPACO PARA JOGAR DE NOVO", True, BRANCO)
        tela.blit(prompt_surf, (btn_x + (btn_w - prompt_surf.get_width()) // 2, btn_y + 13))
