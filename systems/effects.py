"""Particle effects and special effects"""
import pygame
import math
from utils.vector import Vector2

class ParticleEffect:
    """Visual particle effect"""
    
    def __init__(self, x, y, lifetime, color):
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.particles = []
    
    def create_particles(self, count, speed_range, direction=None):
        """Create particles"""
        import random
        for _ in range(count):
            if direction is None:
                angle = random.uniform(0, 2 * math.pi)
            else:
                angle = direction + random.uniform(-0.5, 0.5)
            
            speed = random.uniform(speed_range[0], speed_range[1])
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': vx,
                'vy': vy,
                'age': 0,
            })
    
    def update(self, dt):
        """Update particle effect"""
        self.lifetime -= dt
        
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['age'] += dt
            particle['vy'] += 9.8 * dt  # Gravity
        
        # Remove old particles
        self.particles = [p for p in self.particles if p['age'] < self.max_lifetime]
    
    def is_alive(self):
        return self.lifetime > 0
    
    def draw(self, surface, camera_offset):
        """Draw particle effect"""
        for particle in self.particles:
            alpha = 1 - (particle['age'] / self.max_lifetime)
            size = max(1, int(4 * alpha))
            
            screen_x = int(particle['x'] - camera_offset.x)
            screen_y = int(particle['y'] - camera_offset.y)
            
            color = tuple(int(c * alpha) for c in self.color)
            pygame.draw.circle(surface, color, (screen_x, screen_y), size)

class EffectSystem:
    """Manages all particle effects"""
    
    def __init__(self):
        self.effects = []
    
    def spawn_damage_effect(self, x, y):
        """Spawn damage effect"""
        effect = ParticleEffect(x, y, 0.5, (255, 0, 0))
        effect.create_particles(10, (50, 150))
        self.effects.append(effect)
    
    def spawn_heal_effect(self, x, y):
        """Spawn healing effect"""
        effect = ParticleEffect(x, y, 0.5, (0, 255, 0))
        effect.create_particles(10, (50, 150))
        self.effects.append(effect)
    
    def spawn_level_up_effect(self, x, y):
        """Spawn level up effect"""
        effect = ParticleEffect(x, y, 1.0, (255, 200, 0))
        effect.create_particles(20, (100, 200))
        self.effects.append(effect)
    
    def spawn_boss_attack_effect(self, x, y, color):
        """Spawn boss attack effect"""
        effect = ParticleEffect(x, y, 0.8, color)
        effect.create_particles(15, (200, 300))
        self.effects.append(effect)
    
    def update(self, dt):
        """Update all effects"""
        for effect in self.effects:
            effect.update(dt)
        
        self.effects = [e for e in self.effects if e.is_alive()]
    
    def draw(self, surface, camera_offset):
        """Draw all effects"""
        for effect in self.effects:
            effect.draw(surface, camera_offset)
