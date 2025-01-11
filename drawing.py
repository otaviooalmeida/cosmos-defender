import pyxel

# Textos para as diferentes telas do jogo

def draw_game_over(self): # Lógica para escrever o menu de game over do jogo
    pyxel.text(44, 35, "VOCE PERDEU :(", pyxel.frame_count % 16)
    pyxel.text(42, 60, f"Score total: {self.score}", 7)
    pyxel.text(25, 90, f"'M' para voltar ao menu", 3)
    pyxel.text(40, 105, f"'ESC' para sair", 2)

def draw_menu(): # Lógica para escrever o menu do jogo
    pyxel.cls(0)
    pyxel.text(44, 40, "COSMOS DEFENDER", pyxel.frame_count % 17)
    pyxel.text(42, 70, "'I' para iniciar", 3)
    pyxel.text(42, 85, "'ESC' para sair", 2)

def draw_boss_death(self): # Tela de vitória quando o boss morre
    pyxel.cls(0)
    pyxel.text(30, 20, "PARABENS, VOCE VENCEU!", pyxel.frame_count % 16)
    pyxel.text(32, 35, "OBRIGADO POR JOGAR :)", pyxel.frame_count % 15)
    pyxel.text(42, 60, f"Score total: {self.score}", 7)
    pyxel.text(25, 90, f"'M' para voltar ao menu", 3)
    pyxel.text(40, 105, f"'ESC' para sair", 2)
    

