# Atributos iniciais do jogador

def initial_attributes(self):
    self.game_over = False
    self.boss_death = False
    self.sound_played = False  # Reseta o som para não haver superposição ou bugs
    # Listas criadas para os respectivos lasers, inimigos e power ups que são adicionados com o decorrer do jogo
    self.bosses = []
    self.red_ships = []
    self.blue_ships = []
    self.asteroids = []
    self.lasers = []
    self.red_lasers = []
    self.blue_lasers = []
    self.orange_lasers = []
    self.power_ups = []
    self.laser_speed = 2 # Velocidade do laser
    self.enemy_speed = 1  # Velocidade inicial dos inimigos
    self.score = 0
    self.lives = 5 # Vidas iniciais do jogador
    self.last_shot_time = 0 # Marcar o momento do último tiro disparado 
    self.level = 1
    self.laser_cooldown = 12 - (self.level * 0.25) # Cooldown do tiro
    self.power_up_active = False # O power up começa como falso 
    self.power_up_timer = 0
    self.min_distance = 10 # Distância mínima para inimigos não spawnarem no mesmo pixel
    self.asteroid_spawn_interval = 95 # Intervalos de spawn dos inimigos
    self.blue_ship_spawn_interval = 220
    self.red_ship_spawn_interval = 185
    self.red_ship_shoot_interval = 90 # Intervalo de disparo dos inimigos
    self.blue_ship_shoot_interval = 90
    self.boss_shoot_interval = 60
    self.last_asteroid_spawn = 0
    self.last_red_ship_spawn = 0
    self.last_blue_ship_spawn = 0
    self.last_blue_shot = 0
    self.last_red_shot = 0
    self.last_boss_shot = 0
    self.blue_laser = None # Definição nula dos lasers para ser possível acessá-los inicialmente
    self.red_laser = None
    self.boss_laser = None
    self.boss_active = False
    self.boss_health = 100