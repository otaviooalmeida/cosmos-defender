from dataclasses import dataclass

@dataclass
class Position:
    """Componente para posição (x, y) de uma entidade."""
    x: float
    y: float

@dataclass
class Velocity:
    """Componente para velocidade (vx, vy) de uma entidade."""
    x: float = 0.0
    y: float = 0.0

@dataclass
class Sprite:
    """Componente para informações de desenho (sprite)."""
    sprite_type: str  # Ex: 'player', 'asteroid', 'blue_ship'
    width: int
    height: int

@dataclass
class Player:
    """Componente para marcar a entidade do jogador e seus atributos únicos."""
    lives: int = 5
    score: int = 0
    laser_cooldown: float = 12.0
    last_shot_time: int = 0

@dataclass
class Enemy:
    """Componente para marcar uma entidade como inimiga."""
    enemy_type: str  # Ex: 'asteroid', 'blue_ship', 'red_ship'

@dataclass
class Boss:
    """Componente para o Boss, com seus atributos específicos."""
    health: int = 100
    max_health: int = 100
    last_shot: int = 0
    direction: int = 1 # 1 para direita, -1 para esquerda

@dataclass
class Laser:
    """Componente para marcar uma entidade como um laser."""
    laser_type: str  # Ex: 'player', 'red', 'blue', 'orange'

@dataclass
class PowerUp:
    """Componente para marcar um power-up e seu tipo."""
    power_type: str  # Ex: 'attack_speed', 'extra_life'

@dataclass
class Shooter:
    """Componente para inimigos que disparam."""
    shoot_interval: int
    last_shot: int = 0

@dataclass
class PowerUpEffect:
    """Componente para gerenciar o estado de um power-up ativo no jogador."""
    active: bool = False
    start_time: int = 0
    duration: int = 300  # Duração em frames (5 segundos a 60fps)
    effect_type: str = ''