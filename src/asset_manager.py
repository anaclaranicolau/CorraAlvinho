"""
Gerenciador centralizado de assets (imagens, sons, músicas e fontes).
Carrega e otimiza todos os recursos na inicialização.
"""
import os
import random
import pygame
from src.config import DIRETORIO_SPRITES, DIRETORIO_SOUNDS, DIRETORIO_ASSETS, LARGURA, ALTURA


class AssetManager:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(AssetManager, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        self._inicializado = True

        self.imagens = {}
        self.sons = {}
        self.fontes = {}

        self.musica_ligada = True
        self.sons_ligados = True
        self.volume_musica = 0.55
        self.volume_sfx = 0.75

        self.carregar_tudo()

    def carregar_tudo(self):
        self._carregar_fontes()
        self._carregar_imagens()
        self._carregar_audio()

    def _carregar_fontes(self):
        # Tenta fontes do sistema para um visual premium
        def obter_fonte(nome, tamanho, negrito=False):
            caminho = pygame.font.match_font(nome)
            if caminho:
                try:
                    f = pygame.font.Font(caminho, tamanho)
                    f.set_bold(negrito)
                    return f
                except Exception:
                    pass
            f = pygame.font.Font(None, tamanho)
            f.set_bold(negrito)
            return f

        self.fontes["titulo"] = obter_fonte("trebuchetms", 64, negrito=True)
        self.fontes["subtitulo"] = obter_fonte("segoeui", 32, negrito=True)
        self.fontes["media"] = obter_fonte("segoeui", 26, negrito=True)
        self.fontes["normal"] = obter_fonte("segoeui", 20)
        self.fontes["pequena"] = obter_fonte("segoeui", 16)
        self.fontes["digital"] = obter_fonte("consola", 24, negrito=True)
        self.fontes["digital_grande"] = obter_fonte("consola", 34, negrito=True)

    def _carregar_imagens(self):
        # Sprites pré-processados
        sprite_defs = {
            "alvinho_run0": ("alvinho_run0.png", (96, 79)),
            "alvinho_run1": ("alvinho_run1.png", (102, 79)),
            "alvinho_jump": ("alvinho_jump.png", (92, 101)),
            "alvinho_hurt": ("alvinho_hurt.png", (90, 79)),
            "banheira": ("obstaculo_banheira.png", (94, 85)),
            "shampoo": ("obstaculo_shampoo.png", (64, 60)),
            "petisco": ("item_petisco.png", (50, 46)),
            "brinquedo": ("item_brinquedo.png", (46, 54)),
        }

        for chave, (arquivo, tamanho) in sprite_defs.items():
            caminho = os.path.join(DIRETORIO_SPRITES, arquivo)
            if os.path.exists(caminho):
                surf = pygame.image.load(caminho).convert_alpha()
                surf_escalada = pygame.transform.smoothscale(surf, tamanho)
                self.imagens[chave] = surf_escalada
            else:
                # Superfície de fallback caso o arquivo não exista
                surf = pygame.Surface(tamanho, pygame.SRCALPHA)
                surf.fill((255, 100, 100, 200))
                self.imagens[chave] = surf

        # Fundos de cenário
        caminho_dia = os.path.join(DIRETORIO_ASSETS, "background_day.jpg")
        if os.path.exists(caminho_dia):
            surf_dia = pygame.image.load(caminho_dia).convert()
            # Escala para preencher a largura e altura mantendo proporção
            self.imagens["bg_dia"] = pygame.transform.smoothscale(surf_dia, (LARGURA, ALTURA))
        else:
            self.imagens["bg_dia"] = None

        caminho_noite = os.path.join(DIRETORIO_ASSETS, "background_night.jpg")
        if os.path.exists(caminho_noite):
            surf_noite = pygame.image.load(caminho_noite).convert()
            self.imagens["bg_noite"] = pygame.transform.smoothscale(surf_noite, (LARGURA, ALTURA))
        else:
            self.imagens["bg_noite"] = None

    def _carregar_audio(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception as e:
                print(f"Aviso: Não foi possível inicializar áudio: {e}")
                return

        arquivos_sfx = {
            "latido": "latido.wav",
            "latido_alto": "latido_alto.wav",
            "pulo": "pulo.wav",
            "derrota": "derrota.wav",
            "milestone": "milestone.wav",
        }

        for nome, arq in arquivos_sfx.items():
            caminho = os.path.join(DIRETORIO_SOUNDS, arq)
            if os.path.exists(caminho):
                try:
                    snd = pygame.mixer.Sound(caminho)
                    snd.set_volume(self.volume_sfx)
                    self.sons[nome] = snd
                except Exception as e:
                    print(f"Erro ao carregar som {arq}: {e}")

        # Música de fundo
        self.caminho_musica = os.path.join(DIRETORIO_SOUNDS, "musica_fundo.mp3")

    def tocar_musica(self):
        if not self.musica_ligada or not os.path.exists(self.caminho_musica):
            return
        try:
            pygame.mixer.music.load(self.caminho_musica)
            pygame.mixer.music.set_volume(self.volume_musica)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao tocar música: {e}")

    def parar_musica(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def alternar_som(self):
        self.sons_ligados = not self.sons_ligados
        self.musica_ligada = self.sons_ligados
        if self.musica_ligada:
            self.tocar_musica()
        else:
            self.parar_musica()
        return self.sons_ligados

    def tocar_som(self, nome):
        if not self.sons_ligados:
            return
        snd = self.sons.get(nome)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def tocar_latido(self):
        if not self.sons_ligados:
            return
        opcao = random.choice(["latido", "latido_alto"])
        self.tocar_som(opcao)

    def tocar_pulo(self):
        self.tocar_som("pulo")

    def tocar_derrota(self):
        self.tocar_som("derrota")

    def tocar_milestone(self):
        self.tocar_som("milestone")
