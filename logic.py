import pyxel
from math import sqrt
from classes import Enemy, PowerUp
from shooting import Shooter
from random import choice
from collisions import collision

class Logic:
    def update_asteroids(self):
        for asteroid in self.asteroids[:]:  # Se o inimigo sair da tela, o jogador perde uma vida
            if not asteroid.update(self.enemy_speed):
                self.asteroids.remove(asteroid)
                self.lives -= 1

        # Gerar novos asteroides
        if pyxel.frame_count - self.last_asteroid_spawn >= self.asteroid_spawn_interval:  # Verificar delay de spawn
            while True:
                new_x = pyxel.rndi(8, 140)  # Aleatorizar as coordenadas de spawn
                if self.level < 10:
                    new_y = 0  # Sempre no y = 0, topo da tela
                if self.level == 10:
                    new_y = 23  # Se nível 10, spawna na altura do boss
                is_valid = True
                for asteroid in self.asteroids:
                    distance = sqrt((asteroid.x - new_x) ** 2 + (asteroid.y - new_y) ** 2)  # Impedir spawn mútuo de asteroides
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for blue_ship in self.blue_ships:
                    distance = sqrt((blue_ship.x - new_x) ** 2 + (blue_ship.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que nave azul
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for red_ship in self.red_ships:
                    distance = sqrt((red_ship.x - new_x) ** 2 + (red_ship.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que nave vermelha
                    if distance < self.min_distance:
                        is_valid = False
                        break
                if is_valid:  # Se não existir dois no mesmo pixel, cria outro
                    self.asteroids.append(Enemy(new_x, new_y, 'asteroid'))
                    break
            self.last_asteroid_spawn = pyxel.frame_count  # Reseta o delay de spawn

    def update_blue_ships(self):
        for blue_ship in self.blue_ships[:]:
            if not blue_ship.update(self.enemy_speed):
                self.blue_ships.remove(blue_ship)
                self.lives -= 1

        # Gerar naves azuis
        if pyxel.frame_count - self.last_blue_ship_spawn >= self.blue_ship_spawn_interval:  # Adaptar delay de spawn da nave azul inimiga
            while True:
                new_x = pyxel.rndi(8, 140)
                if self.level < 10:
                    new_y = 0
                if self.level == 10:
                    new_y = 23
                is_valid = True
                for blue_ship in self.blue_ships:
                    distance = sqrt((blue_ship.x - new_x) ** 2 + (blue_ship.y - new_y) ** 2)
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for asteroid in self.asteroids:
                    distance = sqrt((asteroid.x - new_x) ** 2 + (asteroid.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que asteroide
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for red_ship in self.red_ships:
                    distance = sqrt((red_ship.x - new_x) ** 2 + (red_ship.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que nave vermelha
                    if distance < self.min_distance:
                        is_valid = False
                        break
                if is_valid:
                    self.blue_ships.append(Enemy(new_x, new_y, 'blue_ship'))
                    break
            self.last_blue_ship_spawn = pyxel.frame_count

    def update_red_ships(self):
        for red_ship in self.red_ships[:]:
            if not red_ship.update(self.enemy_speed):
                self.red_ships.remove(red_ship)
                self.lives -= 1

        # Gerar novas naves vermelhas
        if pyxel.frame_count - self.last_red_ship_spawn >= self.red_ship_spawn_interval:
            while True:  # Mesma lógica usada para gerar as naves azuis
                new_x = pyxel.rndi(8, 140)
                if self.level < 10:
                    new_y = 0
                if self.level == 10:
                    new_y = 23  # Spawnar no mesmo pixel y do boss no nível 10
                is_valid = True
                for red_ship in self.red_ships:
                    distance = sqrt((red_ship.x - new_x) ** 2 + (red_ship.y - new_y) ** 2)
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for asteroid in self.asteroids:
                    distance = sqrt((asteroid.x - new_x) ** 2 + (asteroid.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que asteroide
                    if distance < self.min_distance:
                        is_valid = False
                        break
                for blue_ship in self.blue_ships:
                    distance = sqrt((blue_ship.x - new_x) ** 2 + (blue_ship.y - new_y) ** 2)  # Impedir spawn no mesmo pixel que nave azul
                    if distance < self.min_distance:
                        is_valid = False
                        break
                if is_valid:
                    self.red_ships.append(Enemy(new_x, new_y, 'red_ship'))
                    break
            self.last_red_ship_spawn = pyxel.frame_count


    def update_lasers(self):  # Movimento dos lasers
        for laser in self.lasers:
            laser["y"] -= self.laser_speed

        self.lasers = [laser for laser in self.lasers if laser["y"] > 0]  # Remove todos os lasers que a coordenada y seja 0 ou menor

    def update_enemy_lasers(self):  # Lógica do laser inimigo
        for red_laser in self.red_lasers[:]:
            red_laser["y"] += self.laser_speed  # Movimento
            if red_laser["y"] > pyxel.height:
                self.red_lasers.remove(red_laser)  # Remove se o laser sair da tela

        for blue_laser in self.blue_lasers[:]:
            blue_laser["y"] += self.laser_speed
            if blue_laser["y"] > pyxel.height:
                self.blue_lasers.remove(blue_laser)

        for orange_laser in self.orange_lasers[:]:
            orange_laser["y"] += self.laser_speed
            if orange_laser["y"] > pyxel.height:
                self.orange_lasers.remove(orange_laser)


    def update_level(self):
        if self.score >= self.level * 25 and self.level < 10: # Aumento da dificuldade conforme o nível
            self.level += 1
            self.laser_cooldown -= 0.5
            self.red_ship_spawn_interval -= 16
            self.blue_ship_spawn_interval -= 16

            # Spawna um power-up de vida extra a cada novo nível
            self.power_ups.append(PowerUp(pyxel.rndi(10, pyxel.width - 15), 0, 'extra_life'))

        if self.level == 10: # Spawn de inimigos fixo quando atinge o nível máximo
            self.red_ship_spawn_interval = 200
            self.blue_ship_spawn_interval = 165
            self.asteroid_spawn_interval = 100


    def update_power_ups(self):
        self.power_ups = [pu for pu in self.power_ups if pu.update(self.enemy_speed)] # Loop encadeado para movimento do power up

        if self.power_up_active and pyxel.frame_count - self.power_up_timer >= 200:  # 10 segundos de duração
            self.power_up_active = False # Desativa após 10 segundos
            self.laser_cooldown = 12 - (self.level * 0.25)  # Volta ao normal
            self.enemy_speed = 1 


    def spawn_power_up(self):
        if self.level >= 2 and len(self.power_ups) < 3:  # Limitar número de power-ups ativos
            if pyxel.frame_count % 500 == 0:
                power_up_type = choice(['attack_speed', 'decrease_enemy_speed']) # Escolha randômica de power ups
                self.power_ups.append(PowerUp(pyxel.rndi(10, pyxel.width - 15), 0, power_up_type))


    def update_logic(self): # Principal lógica do jogo
        if self.in_menu: # Lógica do menu
            if pyxel.btnp(pyxel.KEY_I): # Se a tecla I for apertada, começa o jogo
                self.in_menu = False
                self.reset_game()
                self.start_game()
            if pyxel.btnp(pyxel.KEY_ESCAPE): # Se a tecla ESC for apertada, sai do jogo
                pyxel.quit()
            return

        if self.game_over: # Chama o método para lidar com a derrota no jogo
            self.handle_game_over()
            return
        
        if self.boss_death: # Chama o método para lidar com a vitória no jogo
            self.handle_boss_death()
            return
        
        # Métodos utilizados
        self.player.move()
        collision(self)
        Logic.spawn_power_up(self)
        Logic.update_power_ups(self)
        Logic.update_lasers(self)
        Logic.update_blue_ships(self)
        Logic.update_red_ships(self)
        Logic.update_asteroids(self)
        Logic.update_enemy_lasers(self)
        Shooter.handle_laser_shooting(self)
        Shooter.red_ship_shoot(self)
        Shooter.blue_ship_shoot(self)

        if self.level < 10: # Nível 10 é o nível máximo
             Logic.update_level(self)

        if self.level == 10 and self.boss_active == False: # Spawna o boss apenas uma vez
            self.boss_active = True
            pyxel.play(0, 3, loop=True) # Música muda quando o boss aparece
            self.update_final_boss()

        if self.level == 10: # Atualiza o tiro do boss sempre
            Shooter.boss_shoot(self)