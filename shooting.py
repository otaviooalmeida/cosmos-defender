import pyxel

class Shooter:

    def red_ship_shoot(self): # Lógica para a nave vermelha inimiga atirar
        if pyxel.frame_count - self.last_red_shot >= self.red_ship_shoot_interval: # Adaptar lógica ao delay de tiro
            for red_ship in self.red_ships:
                self.red_laser = {"x": red_ship.x + 2, "y": red_ship.y + 4} # Coordenadas de onde o tiro deve sair
                self.red_lasers.append(self.red_laser) # Adicionar o tiro a lista de lasers
                break
            self.last_red_shot = pyxel.frame_count  # Atualiza o último disparo do laser vermelho


    def blue_ship_shoot(self): # Lógica para a nave azul inimiga atirar
        if pyxel.frame_count - self.last_blue_shot >= self.blue_ship_shoot_interval:
            for blue_ship in self.blue_ships:
                self.blue_laser = {"x": blue_ship.x + 2, "y": blue_ship.y + 4}
                self.blue_lasers.append(self.blue_laser)
                break
            self.last_blue_shot = pyxel.frame_count


    # Mecânica de tiro do boss
    def boss_shoot(self):
        if pyxel.frame_count - self.last_boss_shot >= self.boss_shoot_interval: # Delay de tiro
            for boss in self.bosses:
                self.boss_laser1 = {"x": boss.x + 2, "y": boss.y + 16} # Primeiro laser
                self.boss_laser2 = {"x": boss.x + 15, "y": boss.y + 16} # Segundo laser
                self.orange_lasers.append(self.boss_laser1)
                self.orange_lasers.append(self.boss_laser2)
                break
            self.last_boss_shot = pyxel.frame_count # Reseta delay de tiro


    def shoot(self): # Lógica para a nave do jogador atirar
        if pyxel.frame_count - self.last_shot_time >= self.laser_cooldown: # Delay de tiro
            self.lasers.append({"x": self.player.x + 3, "y": self.player.y})
            self.last_shot_time = pyxel.frame_count
            pyxel.play(1, 2, loop=False) # Som do tiro do jogador
            self.sound_played = False

    def handle_laser_shooting(self): # Atirar na tecla 'ESPAÇO'
        if pyxel.btnp(pyxel.KEY_SPACE):
            Shooter.shoot(self)