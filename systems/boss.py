"""Boss arena and boss mechanics"""
import random
import math
from utils.vector import Vector2

class BossArena:
    """Arena where boss fights take place"""
    
    def __init__(self, boss_x, boss_y, arena_radius=300):
        self.boss_x = boss_x
        self.boss_y = boss_y
        self.arena_radius = arena_radius
        self.active = False
        self.difficulty_level = 1
    
    def enter_arena(self, player, boss):
        """Check if player entered boss arena"""
        distance = math.sqrt((player.pos.x - self.boss_x) ** 2 + 
                            (player.pos.y - self.boss_y) ** 2)
        if distance < self.arena_radius and not self.active:
            self.active = True
            boss.health = boss.max_health  # Reset boss health
            return True
        return False
    
    def exit_arena(self, player):
        """Check if player left arena"""
        distance = math.sqrt((player.pos.x - self.boss_x) ** 2 + 
                            (player.pos.y - self.boss_y) ** 2)
        if distance > self.arena_radius * 1.2:
            self.active = False
            return True
        return False
    
    def draw(self, surface, camera_offset):
        """Draw arena boundary (optional visual)"""
        if self.active:
            import pygame
            screen_x = int(self.boss_x - camera_offset.x)
            screen_y = int(self.boss_y - camera_offset.y)
            pygame.draw.circle(surface, (255, 100, 0), (screen_x, screen_y), 
                              self.arena_radius, 2)

class BossAI:
    """AI behavior for bosses"""
    
    def __init__(self, boss):
        self.boss = boss
        self.attack_pattern = 0
        self.pattern_timer = 0
        self.pattern_duration = 3
    
    def update(self, dt, player, arena):
        """Update boss AI"""
        if not arena.active:
            return
        
        self.pattern_timer += dt
        
        # Change attack pattern every 3 seconds
        if self.pattern_timer >= self.pattern_duration:
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.pattern_timer = 0
        
        distance = self.boss.distance_to(player)
        
        if self.attack_pattern == 0:
            # Chase player
            direction = (player.pos - self.boss.pos).normalize()
            self.boss.vel = direction * self.boss.speed
        
        elif self.attack_pattern == 1:
            # Circle strafe
            angle = math.atan2(player.pos.y - self.boss.pos.y, 
                              player.pos.x - self.boss.pos.x)
            angle += dt * 2
            new_x = player.pos.x + math.cos(angle) * 150
            new_y = player.pos.y + math.sin(angle) * 150
            
            target = Vector2(new_x, new_y)
            direction = (target - self.boss.pos).normalize()
            self.boss.vel = direction * self.boss.speed * 0.8
        
        elif self.attack_pattern == 2:
            # Retreat and attack
            direction = (player.pos - self.boss.pos).normalize()
            self.boss.vel = direction * -self.boss.speed * 0.5
    
    def get_phase_bonus(self):
        """Get damage bonus based on boss phase"""
        if self.boss.phase == 1:
            return 1.0
        elif self.boss.phase == 2:
            return 1.3
        else:  # Phase 3
            return 1.5

class BossReward:
    """Reward for defeating a boss"""
    
    def __init__(self, boss_type):
        self.boss_type = boss_type
        self.items = self._get_boss_loot()
    
    def _get_boss_loot(self):
        """Get loot based on boss type"""
        loot_tables = {
            'fire_elemental': {'diamond': 3, 'gold': 10, 'iron': 20},
            'ice_golem': {'diamond': 2, 'gold': 8, 'iron': 15},
            'dark_lord': {'diamond': 5, 'gold': 15, 'iron': 25},
        }
        return loot_tables.get(self.boss_type, {'gold': 5, 'diamond': 1})
    
    def give_reward(self, player):
        """Give reward to player"""
        player.gain_experience(500)
        for item, quantity in self.items.items():
            player.inventory.add_item(item, quantity)
