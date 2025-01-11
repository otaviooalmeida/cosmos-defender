######## ARQUIVO PRINCIPAL DO JOGO "COSMOS DEFENDER" ########
# Otávio Almeida - 169502

import pyxel
from logic import Logic
from classes import Ship, Boss
from attributes import initial_attributes
import drawing

boss = Boss(50, 6, 'final_boss') # Variável global boss


class MainGame:
    def __init__(self):
        pyxel.init(150, 150, title="Cosmos Defender")
        pyxel.sound(0)  # Carrega o som do banco de dados de sons
        pyxel.load("my_resource.pyxres")
        self.in_menu = True  # Adiciona a variável para controle do menu
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self): # Atributos iniciais do jogo
        self.player = Ship(60, 120)
        initial_attributes(self)

    def update(self): # Lógica principal do jogo
        Logic.update_logic(self)
        global boss # Declara variável global
        boss.update(speed=2)


    def start_game(self):
        pyxel.play(0, 1, loop=True)  # Toca o som do índice 1 no canal 0 em loop
        self.in_menu = False # Seta todos as instâncias de tela diferentes para falsos
        self.game_over = False
        self.sound_played = False
        self.boss_death = False


    def handle_game_over(self):
        if not self.sound_played:  # Verifica se o som já foi tocado
            pyxel.play(0, 0, loop=False)  # Toca o som de game over
            self.sound_played = True  # Marca como tocado

        if pyxel.btnp(pyxel.KEY_M):  # Voltar ao menu
            self.in_menu = True
            self.sound_played = False  # Reseta para tocar novamente no futuro

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit() # Se 'ESC', fecha o jogo


    def handle_boss_death(self):
        if not self.sound_played:  # Verifica se o som já foi tocado
            pyxel.play(0, 4, loop=False)  # Toca o som de game over
            self.sound_played = True  # Marca como tocado

        if pyxel.btnp(pyxel.KEY_M):  # Voltar ao menu
            self.in_menu = True
            self.sound_played = False  # Reseta para tocar novamente no futuro

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit() # Se 'ESC', fecha o jogo

    def update_final_boss(self):
        self.bosses.append(boss) # Adiciona a variável local boss à lista bosses para desenhá-lo

    def activate_power_up(self, power_type):
        self.power_up_active = True
        self.power_up_timer = pyxel.frame_count
        if power_type == 'attack_speed':
            self.laser_cooldown = 4  # Reduz cooldown para maior velocidade de tiro
        elif power_type == 'decrease_enemy_speed':
            self.enemy_speed = 0.5
        elif power_type == 'extra_life':
            self.lives += 1  # Incrementa a vida do jogador


# Função que chama todas as funções necessárias para desenhar o jogo (parte visível)
    def draw(self):
        pyxel.cls(0)
        if self.in_menu:
            drawing.draw_menu()
            return
        elif self.game_over:
            drawing.draw_game_over(self)
            return
        elif self.boss_death:
            drawing.draw_boss_death(self)
            return

        pyxel.blt(0, 0, 1, 0, 0, 150, 150)
        pyxel.blt(self.player.x, self.player.y, 2, 6, 6, 8, 7)

        #Desenho dos inimigos e lasers
        for asteroid in self.asteroids:
            asteroid.draw()
        for blue_ship in self.blue_ships:
            blue_ship.draw()
        for red_ship in self.red_ships:
            red_ship.draw()
        for boss in self.bosses:
            boss.draw()

        for laser in self.lasers:
            pyxel.rect(laser["x"], laser["y"], 1.5, 5, 4)

        for red_laser in self.red_lasers:
            pyxel.rect(red_laser["x"], red_laser["y"], 1.5, 5, 8)
            break 
        for blue_laser in self.blue_lasers:
            pyxel.rect(blue_laser["x"], blue_laser["y"], 1.5, 5, 12)
            break
        for orange_laser in self.orange_lasers:
            pyxel.rect(orange_laser["x"], orange_laser["y"], 2, 6, 9)


        # Desenha os power-ups
        for power_up in self.power_ups:
            power_up.draw()

        pyxel.text(5, 15, f"Nivel: {self.level}", 10)
        pyxel.text(5, 5, f"Vidas: {self.lives}", 7)


if __name__ == "__main__":
    MainGame()
