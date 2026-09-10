"""Player entity"""
import math
from config import PLAYER_SPEED, PLAYER_HEALTH, PLAYER_SIZE, PLAYER_ATTACK_RANGE, PLAYER_ATTACK_COOLDOWN, PLAYER_ATTACK_DAMAGE
from entities.entity import Entity
from systems.crafting import Inventory
from utils.vector import Vector2

class Player(Entity):
    """Player character"""
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, PLAYER_HEALTH, (100, 200, 255))
        self.inventory = Inventory(max_slots=30)
        self.selected_weapon = None
        self.attack_cooldown = 0
        self.attack_range = PLAYER_ATTACK_RANGE
        self.attack_damage = PLAYER_ATTACK_DAMAGE
        self.direction = Vector2(1, 0)
        self.level = 1
        self.experience = 0
        self.hunger = 100
        self.max_hunger = 100
    
    def handle_input(self, keys):
        """Handle player input"""
        self.vel = Vector2(0, 0)
        
        if keys.get('w'):
            self.vel.y -= PLAYER_SPEED
        if keys.get('s'):
            self.vel.y += PLAYER_SPEED
        if keys.get('a'):
            self.vel.x -= PLAYER_SPEED
        if keys.get('d'):
            self.vel.x += PLAYER_SPEED
        
        if self.vel.magnitude() > 0:
            self.direction = self.vel.normalize()
    
    def update(self, dt, world, camera):
        """Update player state"""
        super().update(dt, world)
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        # Update hunger
        self.hunger = max(0, self.hunger - dt * 5)
        if self.hunger <= 0:
            self.take_damage(dt * 2)
        
        # Camera follows player
        camera.target = self.pos.copy()
    
    def attack(self, entities):
        """Attack nearby entities"""
        if self.attack_cooldown > 0:
            return
        
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        
        for entity in entities:
            if entity is not self and self.distance_to(entity) <= self.attack_range:
                damage = self.attack_damage
                entity.take_damage(damage)
    
    def gain_experience(self, amount):
        """Gain experience"""
        self.experience += amount
        exp_to_level = self.level * 100
        if self.experience >= exp_to_level:
            self.level_up()
    
    def level_up(self):
        """Level up"""
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.heal(10)
        self.attack_damage += 2
    
    def eat(self, food_type):
        """Eat food"""
        hunger_recovery = {
            'apple': 20,
            'meat': 30,
            'bread': 25,
        }
        if food_type in hunger_recovery:
            self.hunger = min(self.hunger + hunger_recovery[food_type], self.max_hunger)
            self.inventory.remove_item(food_type, 1)
    
    def draw(self, surface, camera_offset):
        """Draw player"""
        import pygame
        screen_x = int(self.pos.x - camera_offset.x)
        screen_y = int(self.pos.y - camera_offset.y)
        
        # Draw player
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.size // 2)
        
        # Draw facing direction indicator
        end_x = screen_x + self.direction.x * 15
        end_y = screen_y + self.direction.y * 15
        pygame.draw.line(surface, (255, 255, 0), (screen_x, screen_y), (end_x, end_y), 2)
        
        # Draw health bar
        bar_width = self.size
        bar_height = 4
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 10, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 10, 
                          bar_width * health_percentage, bar_height))
        
        # Draw hunger bar
        hunger_percentage = self.hunger / self.max_hunger
        pygame.draw.rect(surface, (200, 100, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 5, bar_width, 3))
        pygame.draw.rect(surface, (255, 200, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 5, 
                          bar_width * hunger_percentage, 3))
