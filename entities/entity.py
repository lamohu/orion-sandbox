"""Base entity class"""
import math
from utils.vector import Vector2
from utils.collision import CircleCollider

class Entity:
    """Base class for all entities"""
    
    def __init__(self, x, y, size, health, color):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.size = size
        self.max_health = health
        self.health = health
        self.color = color
        self.collider = CircleCollider(x, y, size / 2)
        self.alive = True
    
    def update(self, dt, world):
        """Update entity state"""
        self.pos = self.pos + self.vel * dt
        self.collider.update_position(self.pos.x, self.pos.y)
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.health = 0
    
    def heal(self, amount):
        """Heal entity"""
        self.health = min(self.health + amount, self.max_health)
    
    def draw(self, surface, camera_offset):
        """Draw entity (override in subclasses)"""
        import pygame
        screen_x = int(self.pos.x - camera_offset.x)
        screen_y = int(self.pos.y - camera_offset.y)
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.size // 2)
        
        # Draw health bar
        bar_width = self.size
        bar_height = 4
        health_percentage = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 10, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 10, 
                          bar_width * health_percentage, bar_height))
    
    def distance_to(self, other):
        """Get distance to another entity"""
        return self.pos.distance_to(other.pos)
