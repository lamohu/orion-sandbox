import pygame
import random
from utils.vector import Vector2

class Particle:
    """Visual particle effect"""
    def __init__(self, x, y, vx, vy, lifetime, color, size):
        self.pos = Vector2(x, y)
        self.vel = Vector2(vx, vy)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
    
    def update(self, dt):
        self.pos = self.pos + self.vel * dt
        self.lifetime -= dt
    
    def is_alive(self):
        return self.lifetime > 0
    
    def draw(self, surface, camera_offset):
        alpha = self.lifetime / self.max_lifetime
        color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(surface, color, self.pos.to_tuple(), self.size)

class ParticleSystem:
    """Manages particle effects"""
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, count, speed_range, lifetime, color, size):
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(speed_range[0], speed_range[1])
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            particle = Particle(x, y, vx, vy, lifetime, color, size)
            self.particles.append(particle)
    
    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, surface, camera_offset):
        for particle in self.particles:
            particle.draw(surface, camera_offset)

import math
