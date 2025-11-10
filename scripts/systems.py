import pyxel
import esper
from math import sqrt
from random import choice
from .components import *

# --- Sistemas de Lógica e Estado ---

class LevelSystem(esper.Processor):
    """Gerencia o avanço de nível, dificuldade e o spawn do Boss."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        if self.game.level >= 10 or self.game.boss_active:
            return

        if not self.world.get_component(Player): return
        # Corrigido: Desempacota o componente diretamente
        player_ent, player = self.world.get_component(Player)[0]
        
        if player.score >= self.game.level * 25:
            self.game.level += 1
            player.laser_cooldown -= 0.5
            self.game.red_ship_spawn_interval -= 16
            self.game.blue_ship_spawn_interval -= 16

            self._spawn_specific_power_up('extra_life')

            if self.game.level == 10:
                self.game.boss_active = True
                pyxel.play(0, 3, loop=True)
                self._spawn_boss()

    def _spawn_specific_power_up(self, power_type):
        x = pyxel.rndi(10, pyxel.width - 15)
        ent = self.world.create_entity()
        self.world.add_component(ent, Position(x, 0))
        self.world.add_component(ent, Velocity(y=self.game.enemy_speed))
        self.world.add_component(ent, PowerUp(power_type))
        self.world.add_component(ent, Sprite(power_type, 5, 4))

    def _spawn_boss(self):
        boss_ent = self.world.create_entity()
        self.world.add_component(boss_ent, Position(pyxel.width / 2 - 8, 15))
        self.world.add_component(boss_ent, Boss())
        self.world.add_component(boss_ent, Sprite('boss', 17, 16))

class PowerUpSystem(esper.Processor):
    """Aplica e remove os efeitos de power-ups."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        if not self.world.get_component(Player): return
            
        # Corrigido: Desempacota o componente diretamente
        player_ent, player = self.world.get_component(Player)[0]
        
        if not self.world.has_component(player_ent, PowerUpEffect):
            self.world.add_component(player_ent, PowerUpEffect())
        
        effect = self.world.component_for_entity(player_ent, PowerUpEffect)

        if effect.active and pyxel.frame_count - effect.start_time >= effect.duration:
            effect.active = False
            if effect.effect_type == 'attack_speed':
                player.laser_cooldown = 12 - (self.game.level * 0.25)
            elif effect.effect_type == 'decrease_enemy_speed':
                self.game.enemy_speed = 1
                for ent, (vel, _) in self.world.get_components(Velocity, Enemy):
                    vel.y = self.game.enemy_speed

# --- Sistemas de Ação e Movimento ---

class PlayerInputSystem(esper.Processor):
    """Processa input do jogador para movimento e tiro."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        if not self.world.get_component(Player): return
        
        player_ent, (pos, player, sprite) = self.world.get_components(Position, Player, Sprite)[0]

        # Movimento
        if pyxel.btn(pyxel.KEY_A) and pos.x > 0: pos.x -= 2
        if pyxel.btn(pyxel.KEY_D) and pos.x < pyxel.width - sprite.width: pos.x += 2
        if pyxel.btn(pyxel.KEY_W) and pos.y > 0: pos.y -= 2
        if pyxel.btn(pyxel.KEY_S) and pos.y < pyxel.height - sprite.height: pos.y += 2

        # Tiro
        if pyxel.btn(pyxel.KEY_SPACE) and (pyxel.frame_count - player.last_shot_time > player.laser_cooldown):
            player.last_shot_time = pyxel.frame_count
            pyxel.play(2, 2)
            self._create_laser(pos.x + 4, pos.y - 4, 'player', 0, -self.game.laser_speed)

    def _create_laser(self, x, y, laser_type, speed_x, speed_y):
        ent = self.world.create_entity()
        self.world.add_component(ent, Position(x, y))
        self.world.add_component(ent, Velocity(x=speed_x, y=speed_y))
        self.world.add_component(ent, Laser(laser_type))
        self.world.add_component(ent, Sprite(f'{laser_type}_laser', 1, 3))

class ShootingSystem(esper.Processor):
    """Controla os disparos dos inimigos e do boss."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        # Inimigos com componente Shooter
        for ent, (pos, shooter, enemy) in self.world.get_components(Position, Shooter, Enemy):
            if pyxel.frame_count - shooter.last_shot > shooter.shoot_interval:
                shooter.last_shot = pyxel.frame_count
                laser_type = 'blue' if enemy.enemy_type == 'blue_ship' else 'red'
                self._create_laser(pos.x + 2, pos.y + 3, laser_type, 0, self.game.laser_speed)
        
        # Boss
        for ent, (pos, boss) in self.world.get_components(Position, Boss):
            if pyxel.frame_count - boss.last_shot > self.game.boss_shoot_interval:
                boss.last_shot = pyxel.frame_count
                self._create_laser(pos.x + 2, pos.y + 16, 'orange', -1, self.game.laser_speed)
                self._create_laser(pos.x + 14, pos.y + 16, 'orange', 1, self.game.laser_speed)

    def _create_laser(self, x, y, laser_type, speed_x, speed_y):
        ent = self.world.create_entity()
        self.world.add_component(ent, Position(x, y))
        self.world.add_component(ent, Velocity(x=speed_x, y=speed_y))
        self.world.add_component(ent, Laser(laser_type))
        self.world.add_component(ent, Sprite(f'{laser_type}_laser', 1, 3))


class MovementSystem(esper.Processor):
    """Move todas as entidades que possuem Posição e Velocidade."""
    def process(self):
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            pos.x += vel.x
            pos.y += vel.y

class BossMovementSystem(esper.Processor):
    """Controla o movimento em zigue-zague do Boss."""
    def process(self):
        for ent, (pos, boss, sprite) in self.world.get_components(Position, Boss, Sprite):
            speed = 1
            pos.x += speed * boss.direction
            if pos.x <= 0 or pos.x >= pyxel.width - sprite.width:
                boss.direction *= -1

# --- Sistemas de Colisão e Limpeza ---

class CollisionSystem(esper.Processor):
    """Verifica e processa todas as colisões do jogo."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        if not self.world.get_component(Player): return
        player_ent, (player_pos, player_comp, player_sprite) = self.world.get_components(Position, Player, Sprite)[0]

        # Colisão: Laser do Jogador vs Inimigos/Boss
        for laser_ent, (laser_pos, laser) in list(self.world.get_components(Position, Laser)):
            if laser.laser_type != 'player': continue

            collided = False
            # vs Inimigos
            for enemy_ent, (enemy_pos, enemy, enemy_sprite) in list(self.world.get_components(Position, Enemy, Sprite)):
                if self._check_collision(laser_pos, enemy_pos, enemy_sprite):
                    self.world.delete_entity(laser_ent, immediate=True)
                    self.world.delete_entity(enemy_ent, immediate=True)
                    player_comp.score += {'asteroid': 1, 'red_ship': 2, 'blue_ship': 3}[enemy.enemy_type]
                    collided = True
                    break
            
            if collided:
                continue

            # vs Boss
            for boss_ent, (boss_pos, boss, boss_sprite) in list(self.world.get_components(Position, Boss, Sprite)):
                if self._check_collision(laser_pos, boss_pos, boss_sprite):
                    self.world.delete_entity(laser_ent, immediate=True)
                    boss.health -= 1
                    if boss.health <= 0:
                        self.world.delete_entity(boss_ent, immediate=True)
                        self.game.boss_death = True
                    break

        # Colisão: Laser Inimigo vs Jogador
        for laser_ent, (laser_pos, laser) in list(self.world.get_components(Position, Laser)):
            if laser.laser_type == 'player': continue
            if self._check_collision(laser_pos, player_pos, player_sprite):
                self.world.delete_entity(laser_ent, immediate=True)
                player_comp.lives -= 1
                break
        
        # Colisão: Inimigo vs Jogador
        for enemy_ent, (enemy_pos, _, enemy_sprite) in list(self.world.get_components(Position, Enemy, Sprite)):
            if self._check_collision(enemy_pos, player_pos, player_sprite):
                self.world.delete_entity(enemy_ent, immediate=True)
                player_comp.lives -= 1
                break

        # Colisão: Power-up vs Jogador
        for pu_ent, (pu_pos, pu, pu_sprite) in list(self.world.get_components(Position, PowerUp, Sprite)):
            if self._check_collision(pu_pos, player_pos, player_sprite):
                self._apply_power_up(player_ent, pu.power_type)
                self.world.delete_entity(pu_ent, immediate=True)
                pyxel.play(3, 4)
                break

    def _check_collision(self, pos1, pos2, sprite2, tolerance=0):
        return (abs(pos1.x - pos2.x) < sprite2.width - tolerance and
                abs(pos1.y - pos2.y) < sprite2.height - tolerance)

    def _apply_power_up(self, player_ent, power_type):
        player = self.world.component_for_entity(player_ent, Player)
        effect = self.world.component_for_entity(player_ent, PowerUpEffect)
        
        if power_type == 'extra_life':
            player.lives += 1
        elif power_type == 'attack_speed':
            effect.active = True
            effect.start_time = pyxel.frame_count
            effect.effect_type = 'attack_speed'
            player.laser_cooldown = 6
        elif power_type == 'decrease_enemy_speed':
            effect.active = True
            effect.start_time = pyxel.frame_count
            effect.effect_type = 'decrease_enemy_speed'
            self.game.enemy_speed = 0.5
            for ent, (vel, _) in self.world.get_components(Velocity, Enemy):
                vel.y = self.game.enemy_speed

class BoundarySystem(esper.Processor):
    """Remove entidades que saem da tela e penaliza o jogador."""
    def process(self):
        if not self.world.get_component(Player): return
        # Corrigido: Desempacota o componente diretamente
        player_ent, player_comp = self.world.get_component(Player)[0]

        for ent, (pos, _) in self.world.get_components(Position, (Enemy, Laser, PowerUp)):
            if not (0 < pos.y < pyxel.height):
                if self.world.has_component(ent, Enemy) and pos.y >= pyxel.height:
                    player_comp.lives -= 1
                self.world.delete_entity(ent, immediate=True)

# --- Sistema de Geração (Spawn) ---

class SpawnSystem(esper.Processor):
    """Responsável por gerar inimigos e power-ups."""
    def __init__(self, game_state):
        self.game = game_state

    def process(self):
        if pyxel.frame_count - self.game.last_asteroid_spawn >= self.game.asteroid_spawn_interval:
            self._spawn_enemy('asteroid', 4, 4)
            self.game.last_asteroid_spawn = pyxel.frame_count
            
        if self.game.boss_active: return

        # Spawn de Inimigos
        if pyxel.frame_count - self.game.last_blue_ship_spawn >= self.game.blue_ship_spawn_interval:
            self._spawn_enemy('blue_ship', 5, 3, self.game.blue_ship_shoot_interval)
            self.game.last_blue_ship_spawn = pyxel.frame_count
        if pyxel.frame_count - self.game.last_red_ship_spawn >= self.game.red_ship_spawn_interval:
            self._spawn_enemy('red_ship', 5, 3, self.game.red_ship_shoot_interval)
            self.game.last_red_ship_spawn = pyxel.frame_count
        
        # Spawn de Power-ups
        if self.game.level >= 2 and pyxel.frame_count % 500 == 0:
            if len(self.world.get_component(PowerUp)) < 3:
                power_up_type = choice(['attack_speed', 'decrease_enemy_speed'])
                self._spawn_power_up(power_up_type)

    def _spawn_enemy(self, enemy_type, width, height, shoot_interval=None):
        while True:
            new_x = pyxel.rndi(8, 140)
            new_y = 0 if self.game.level < 10 else 23
            if self._is_valid_spawn(new_x, new_y):
                ent = self.world.create_entity()
                self.world.add_component(ent, Position(new_x, new_y))
                self.world.add_component(ent, Velocity(y=self.game.enemy_speed))
                self.world.add_component(ent, Enemy(enemy_type))
                self.world.add_component(ent, Sprite(enemy_type, width, height))
                if shoot_interval:
                    self.world.add_component(ent, Shooter(shoot_interval))
                break
    
    def _spawn_power_up(self, power_type):
        x = pyxel.rndi(10, pyxel.width - 15)
        ent = self.world.create_entity()
        self.world.add_component(ent, Position(x, 0))
        self.world.add_component(ent, Velocity(y=self.game.enemy_speed))
        self.world.add_component(ent, PowerUp(power_type))
        self.world.add_component(ent, Sprite(power_type, 5, 4))

    def _is_valid_spawn(self, x, y, min_distance=10):
        for ent, (pos,) in self.world.get_components(Position):
            if sqrt((pos.x - x)**2 + (pos.y - y)**2) < min_distance:
                return False
        return True

# --- Sistema de Renderização ---

class RenderSystem(esper.Processor):
    """Desenha todas as entidades com sprites."""
    def process(self):
        for ent, (pos, sprite) in self.world.get_components(Position, Sprite):
            s_type = sprite.sprite_type
            # Sprites do Jogo
            if s_type == 'player': pyxel.blt(pos.x, pos.y, 2, 6, 6, 8, 7)
            elif s_type == 'asteroid': pyxel.blt(pos.x, pos.y, 2, 51, 11, 4, 4)
            elif s_type == 'red_ship': pyxel.blt(pos.x, pos.y, 2, 35, 11, 5, 3)
            elif s_type == 'blue_ship': pyxel.blt(pos.x, pos.y, 2, 41, 27, 5, 3)
            elif s_type == 'attack_speed': pyxel.blt(pos.x, pos.y, 2, 1, 20, 5, 4)
            elif s_type == 'decrease_enemy_speed': pyxel.blt(pos.x, pos.y, 2, 9, 26, 5, 4)
            elif s_type == 'extra_life': pyxel.blt(pos.x, pos.y, 2, 10, 17, 5, 4)
            # Lasers (usando rect para simplicidade)
            elif s_type == 'player_laser': pyxel.rect(pos.x, pos.y, 1, 3, 7)
            elif s_type == 'red_laser': pyxel.rect(pos.x, pos.y, 1, 3, 8)
            elif s_type == 'blue_laser': pyxel.rect(pos.x, pos.y, 1, 3, 12)
            elif s_type == 'orange_laser': pyxel.rect(pos.x, pos.y, 2, 4, 9)
            # Boss
            elif s_type == 'boss':
                pyxel.blt(pos.x, pos.y, 2, 16, 49, 17, 16)
                if self.world.has_component(ent, Boss):
                    self._draw_health_bar(pos, self.world.component_for_entity(ent, Boss))

    def _draw_health_bar(self, pos, boss_comp):
        bar_width = 17; bar_height = 1; margin_y = -2
        current_bar_width = int((boss_comp.health / boss_comp.max_health) * bar_width)
        pyxel.rect(pos.x, pos.y + margin_y, bar_width, bar_height, 8)
        pyxel.rect(pos.x, pos.y + margin_y, current_bar_width, bar_height, 11)