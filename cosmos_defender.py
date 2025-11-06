import pyxel
import esper
# print(esper.__file__) # Removendo a linha de debug
from scripts.components import *
from scripts.systems import (
    PlayerInputSystem, MovementSystem, BossMovementSystem, BoundarySystem,
    RenderSystem, LevelSystem, PowerUpSystem, ShootingSystem,
    CollisionSystem, SpawnSystem
)

class CosmosDefender:
    def __init__(self):
        pyxel.init(160, 120, title="Cosmos Defender", fps=60)
        pyxel.load("assets/my_resource.pyxres")
        self.setup_game()
        pyxel.run(self.update, self.draw)

    def setup_game(self):
        """Inicializa ou reinicia o estado do jogo e o mundo ECS."""
        # --- Estado Global do Jogo ---
        self.in_menu = True
        self.game_over = False
        self.boss_death = False
        self.level = 1
        self.enemy_speed = 1.0
        self.laser_speed = 3.0
        self.scroll_y = 0 # Variável para o scroll do background

        # Timers de Spawn
        self.last_asteroid_spawn = 0
        self.last_blue_ship_spawn = 0
        self.last_red_ship_spawn = 0

        # Intervalos de Spawn e Disparo
        self.asteroid_spawn_interval = 95
        self.blue_ship_spawn_interval = 220
        self.red_ship_spawn_interval = 185
        self.blue_ship_shoot_interval = 90
        self.red_ship_shoot_interval = 90
        self.boss_shoot_interval = 60
        
        self.boss_active = False

        # --- Configuração do Mundo ECS ---
        self.world = esper.World()
        self.create_player()
        self._register_systems()

    def _register_systems(self):
        """Adiciona todos os sistemas ao mundo ECS na ordem de execução."""
        self.world.add_processor(PlayerInputSystem(self))
        self.world.add_processor(MovementSystem())
        self.world.add_processor(BossMovementSystem())
        self.world.add_processor(ShootingSystem(self))
        self.world.add_processor(SpawnSystem(self))
        self.world.add_processor(CollisionSystem(self))
        self.world.add_processor(PowerUpSystem(self))
        self.world.add_processor(LevelSystem(self))
        self.world.add_processor(BoundarySystem())
        self.render_processor = RenderSystem()
        self.world.add_processor(self.render_processor)

    def create_player(self):
        """Cria a entidade do jogador no mundo."""
        player_ent = self.world.create_entity()
        self.world.add_component(player_ent, Position(x=80, y=100))
        self.world.add_component(player_ent, Sprite(sprite_type='player', width=8, height=8))
        self.world.add_component(player_ent, Player())
        self.world.add_component(player_ent, PowerUpEffect())

    def update(self):
        """Loop de atualização principal."""
        if self.in_menu:
            if pyxel.btnp(pyxel.KEY_I):
                self.in_menu = False
                pyxel.play(0, 5, loop=True)
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()
            return

        if self.game_over or self.boss_death:
            if pyxel.btnp(pyxel.KEY_R):
                self.setup_game()
                self.in_menu = False
                pyxel.play(0, 5, loop=True)
            return

        # Atualiza a posição do background
        self.scroll_y = (self.scroll_y + 0.5) % pyxel.height

        # Processa todos os sistemas
        self.world.process()

        # Verifica condição de Game Over
        if self.world.get_component(Player):
            player_comp = self.world.get_component(Player)[0][1]
            if player_comp.lives <= 0:
                self.game_over = True
                pyxel.stop()
                pyxel.play(2, 6)
        else:
            self.game_over = True
            pyxel.stop()
            pyxel.play(2, 6)


    def draw(self):
        """Loop de desenho principal."""
        pyxel.cls(0)

        if self.in_menu:
            pyxel.text(44, 40, "COSMOS DEFENDER", pyxel.frame_count % 16)
            pyxel.text(42, 70, "'I' para iniciar", 3)
            pyxel.text(42, 85, "'ESC' para sair", 2)
            return

        score = 0
        if self.world.get_component(Player):
            score = self.world.get_component(Player)[0][1].score

        if self.game_over:
            pyxel.text(65, 40, "GAME OVER", 8)
            pyxel.text(50, 60, f"SCORE: {score}", 7)
            pyxel.text(45, 80, "- PRESS R TO RESTART -", 7)
            return
        
        if self.boss_death:
            pyxel.text(50, 40, "PARABENS, VOCE VENCEU!", pyxel.frame_count % 16)
            pyxel.text(52, 60, f"SCORE: {score}", 7)
            pyxel.text(45, 80, "- PRESS R TO RESTART -", 7)
            return

        # --- Desenho do Jogo ---
        # Desenha o background com scroll
        pyxel.blt(0, self.scroll_y, 1, 0, 0, pyxel.width, pyxel.height, 0)
        pyxel.blt(0, self.scroll_y - pyxel.height, 1, 0, 0, pyxel.width, pyxel.height, 0)

        # O RenderSystem cuida de desenhar todas as entidades
        self.render_processor.process()

        # Desenha a UI (Vidas e Pontuação)
        if self.world.get_component(Player):
            player_comp = self.world.get_component(Player)[0][1]
            pyxel.text(5, 5, f"SCORE: {player_comp.score}", 7)
            pyxel.text(120, 5, f"LIVES: {player_comp.lives}", 7)
            pyxel.text(5, 110, f"LEVEL: {self.level}", 7)

if __name__ == "__main__":
    CosmosDefender()