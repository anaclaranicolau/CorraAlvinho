"""
Ponto de entrada do jogo Corra, Alvinho!
Execute com: python main.py
"""
import os
import sys

# Garante o diretório do projeto no sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Jogo


def main():
    jogo = Jogo()
    jogo.executar()


if __name__ == "__main__":
    main()