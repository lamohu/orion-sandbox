"""Enemy entities"""
import random
import math
from config import ENEMY_TYPES
from entities.entity import Entity
from utils.vector import Vector2

class Enemy(Entity):
    """Generic enemy"""
    
    def __init__(self, x, y, enemy_type):
        config = ENEMY_TYPES[enemy_type]
        super().__init__(x, y, config['size'], config['health'], config['color'])
        self.enemy_type = enemy_type
        self.speed = config['speed']
        self.damage = config['damage']
        self.target = None
        self.attack_cooldown = 0
        self.attack_range = 30
        self.wander_timer = random.uniform(0, 5)
        self.wander_direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
    
    def update(self, dt, world, player):
        """Update enemy state"""
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.wander_timer -= dt
        
        distance_to_player = self.distance_to(player)
        
        # Chase player if close
        if distance_to_player < 200:
            direction = (player.pos - self.pos).normalize()
            self.vel = direction * self.speed
            self.target = player
            
            # Attack if in range
            if distance_to_player < self.attack_range and self.attack_cooldown <= 0:
                player.take_damage(self.damage)
                self.attack_cooldown = 1
        else:
            # Wander
            if self.wander_timer <= 0:
                self.wander_timer = random.uniform(2, 5)
                self.wander_direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            
            self.vel = self.wander_direction * self.speed * 0.5
        
        super().update(dt, world)
    
    def draw(self, surface, camera_offset):
        """Draw enemy"""
        super().draw(surface, camera_offset)

class Boss(Entity):
    """Boss enemy"""
    
    def __init__(self, x, y, boss_type):
        from config import BOSSES
        config = BOSSES[boss_type]
        super().__init__(x, y, config['size'], config['health'], config['color'])
        self.boss_type = boss_type
        self.speed = config['speed']
        self.damage = config['damage']
        self.abilities = config['abilities']
        self.ability_cooldowns = {ability: 0 for ability in self.abilities}
        self.attack_range = 50
        self.phase = 1
        self.phase_timer = 0
    
    def update(self, dt, world, player):
        """Update boss state"""
        distance_to_player = self.distance_to(player)
        
        # Update ability cooldowns
        for ability in self.ability_cooldowns:
            self.ability_cooldowns[ability] = max(0, self.ability_cooldowns[ability] - dt)
        
        # Phase changes based on health
        health_percentage = self.health / self.max_health
        if health_percentage < 0.66:
            self.phase = 2
        if health_percentage < 0.33:
            self.phase = 3
        
        # Chase and attack
        if distance_to_player < 300:
            direction = (player.pos - self.pos).normalize()
            self.vel = direction * self.speed
            
            # Use abilities
            if distance_to_player < self.attack_range:
                self._use_ability(player)
        else:
            self.vel = Vector2(0, 0)
        
        super().update(dt, world)
    
    def _use_ability(self, player):
        """Use a random ability"""
        available_abilities = [a for a in self.abilities if self.ability_cooldowns[a] <= 0]
        if available_abilities:
            ability = random.choice(available_abilities)
            self.ability_cooldowns[ability] = 3
            
            if ability == 'fireball':
                damage = self.damage * 1.5
            elif ability == 'ice_spike':
                damage = self.damage * 1.3
            elif ability == 'shadow_bolt':
                damage = self.damage * 1.2
            else:
                damage = self.damage
            
            player.take_damage(damage)
