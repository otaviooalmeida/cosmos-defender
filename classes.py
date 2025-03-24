import pyxel

class Ship:
    def __init__(self, x, y): # Coordenadas
        self.x = x
        self.y = y

    def move(self): # Teclas de movimento
        if pyxel.btn(pyxel.KEY_A) and self.x > 0:
            self.x -= 2
        if pyxel.btn(pyxel.KEY_D) and self.x < pyxel.width - 9.90:
            self.x += 2
        if pyxel.btn(pyxel.KEY_W) and self.y > 0:
            self.y -= 2
        if pyxel.btn(pyxel.KEY_S) and self.y < pyxel.height - 8:
            self.y += 2



class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type

    def update(self, speed): # Movimento do power-up
        self.y += speed
        if self.y >= pyxel.height:
            return False  # Remove power-up se sair da tela
        return True

    def draw(self): # Desenha cada power-up dependendo do seu tipo
        if self.power_type == 'attack_speed': 
            pyxel.blt(self.x, self.y, 2, 1, 20, 5, 4)
        elif self.power_type == 'decrease_enemy_speed':
            pyxel.blt(self.x, self.y, 2, 9, 26, 5, 4)
        elif self.power_type == 'extra_life':
            pyxel.blt(self.x, self.y, 2, 10, 17, 5, 4)



class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

    def update(self, speed): # Movimento do inimigo
        self.y += speed
        if self.y >= pyxel.height:
            return False  # Remove enemy se sair da tela
        return True

    def draw(self): # Desenha o inimigo dependendo de seu tipo
        if self.enemy_type == 'asteroid':
            pyxel.blt(self.x, self.y, 2, 51, 11, 4, 4)
        elif self.enemy_type == 'red_ship':
            pyxel.blt(self.x, self.y, 2, 35, 11, 5, 3)
        elif self.enemy_type == 'blue_ship':
            pyxel.blt(self.x, self.y, 2, 41, 27, 5, 3)
        elif self.enemy_type == 'final_boss':
            pyxel.blt(self.x, self.y, 2, 16, 49, 17, 16)


class Boss:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.direction = 1  # Direção inicial (1 para direita, -1 para esquerda)
        self.max_health = 100  # Vida máxima do boss
        self.current_health = 100  # Vida atual do boss

    def update(self, speed):
        # Movimento horizontal em zigue-zague
        self.x += speed * self.direction

        # Inverter direção se atingir as bordas da tela
        if self.x < 0 or self.x > pyxel.width - 17:
            self.direction *= -1
        return True


    def draw(self):
        # Desenho do boss
        if self.enemy_type == 'final_boss':
            pyxel.blt(self.x, self.y, 2, 16, 49, 17, 16)
        # Desenhar barra de vida abaixo do boss
            self.draw_health_bar()

    def draw_health_bar(self):
        # Configurações da barra de vida
        bar_width = 17  
        bar_height = 1  
        margin_y = -2  # Distância da barra de vida do boss

        # Calcular largura da barra com base na vida atual
        current_bar_width = int((self.current_health / self.max_health) * bar_width)

        # Desenhar a parte vermelha da barra 
        pyxel.rect(self.x, self.y + margin_y, bar_width, bar_height, 8)  # A barra vermelha será a base

        # Desenhar a parte verde da barra (vida restante)
        pyxel.rect(self.x, self.y + margin_y, current_bar_width, bar_height, 11)  # A barra verde vai sobrepor a vermelha

    def take_damage(self, amount): # Método para o dano sofrido do boss
        self.current_health -= amount
        if self.current_health == 0:
            self.boss_death = True
        







        
