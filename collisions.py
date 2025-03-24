def collision(self): 
    for laser in self.lasers[:]: # Se for o inimigo tocando no laser do jogador, o inimigo morre e o jogador pontua
        for asteroid in self.asteroids[:]:
            if (laser["x"] - 2 < asteroid.x + 3 and
                laser["x"] + 3 > asteroid.x - 1 and
                laser["y"] - 1 < asteroid.y + 1 and
                laser["y"] + 1 > asteroid.y - 1):
                self.asteroids.remove(asteroid)
                self.lasers.remove(laser)
                self.score += 1
                break
            
        for red_ship in self.red_ships[:]:
            if (laser["x"] - 2 < red_ship.x + 3 and
                laser["x"] + 2 > red_ship.x - 2 and
                laser["y"]  < red_ship.y + 2 and
                laser["y"] + 2 > red_ship.y - 2):
                self.red_ships.remove(red_ship)
                self.lasers.remove(laser)
                self.score += 5  # Pontuação maior para destruir as naves vermelhas
                break

        for blue_ship in self.blue_ships[:]:
            if (laser["x"] - 2 < blue_ship.x + 3 and
                laser["x"] + 2 > blue_ship.x - 2 and
                laser["y"]  < blue_ship.y + 2 and
                laser["y"] + 2 > blue_ship.y - 2):
                self.blue_ships.remove(blue_ship)
                self.lasers.remove(laser)
                self.score += 5  # Pontuação maior para destruir as naves azuis
                break

        for boss in self.bosses[:]:
            if (laser["x"] - 8 < boss.x + 9 and
                laser["x"] + 4 > boss.x + 1 and  # Ajuste na borda esquerda
                laser["y"] - 10 < boss.y + 5 and
                laser["y"] + 8 > boss.y - 5): 
                # Verificar se o laser atinge a base do boss
                base_y = boss.y + 15  # Base do boss, 15 pixels abaixo do boss(y)
                if laser["y"] + 8 >= base_y:  # Checa se o laser atinge a base
                    boss.take_damage(1)
                    self.boss_health -= 1
                    self.score += 1
                # Remover o laser em qualquer caso
                self.lasers.remove(laser)
                break

    # Se o inimigo atinge o jogador, o jogador perde uma vida e o inimigo morre
    for asteroid in self.asteroids[:]:
        if (self.player.x - 1 < asteroid.x + 5 and
            self.player.x + 8 > asteroid.x - 1 and
            self.player.y - 1 < asteroid.y + 3 and
            self.player.y + 8 > asteroid.y - 1):
            self.asteroids.remove(asteroid)
            self.lives -= 1

    for red_ship in self.red_ships[:]:
        if (self.player.x - 1 < red_ship.x + 4 and
            self.player.x + 4 > red_ship.x - 1 and
            self.player.y - 1 < red_ship.y + 4 and
            self.player.y + 4 > red_ship.y - 1):
            self.red_ships.remove(red_ship)
            self.lives -= 1

    for blue_ship in self.blue_ships[:]:
        if (self.player.x - 1 < blue_ship.x + 4 and
            self.player.x + 4 > blue_ship.x - 1 and
            self.player.y - 1 < blue_ship.y + 4 and
            self.player.y + 4 > blue_ship.y - 1):
            self.blue_ships.remove(blue_ship)
            self.lives -= 1

    for boss in self.bosses[:]:
            if (self.player.x - 8 < boss.x + 9 and
                self.player.x + 4 > boss.x - 5 and
                self.player.y - 10 < boss.y + 5 and
                self.player.y + 8 > boss.y - 5):
                self.lives -= self.lives # Se o jogador encostar no boss, ele automaticamente perde todas as vidas e o jogo acaba
    
    # Se o laser inimigo acerta o jogador, ele perde vida
    for red_laser in self.red_lasers[:]:
        if (self.player.x - 1 < red_laser["x"] < self.player.x + 8 and
            self.player.y - 1 < red_laser["y"] < self.player.y + 8):
            self.red_lasers.remove(red_laser)
            self.lives -= 1

    for blue_laser in self.blue_lasers[:]:
        if (self.player.x - 1 < blue_laser["x"] < self.player.x + 8 and
            self.player.y - 1 < blue_laser["y"] < self.player.y + 8):
            self.blue_lasers.remove(blue_laser)
            self.lives -= 1

    for orange_laser in self.orange_lasers[:]:
        if (self.player.x - 1 < orange_laser["x"] < self.player.x + 8 and
            self.player.y - 1 < orange_laser["y"] < self.player.y + 8):
            self.orange_lasers.remove(orange_laser)
            self.lives -= 3 # Caso seja o laser do boss (laranja), o jogador perde três vidas

    # Colisão dos power ups (velocidade de ataque, lentidão dos inimigos ou vida extra)
    for power_up in self.power_ups[:]:
        if (self.player.x < power_up.x + 5
            and self.player.x + 8 > power_up.x
            and self.player.y < power_up.y + 4
            and self.player.y + 7 > power_up.y):
            self.power_ups.remove(power_up)
            self.activate_power_up(power_up.power_type)

    if self.lives <= 0:
        self.game_over = True # Se o jogador perder todas as vidas, ele perde o jogo

    if self.boss_health <= 0:
        self.boss_death = True # Se o boss perder todas as vidas, o jogador vence o jogo
