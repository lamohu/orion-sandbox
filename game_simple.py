"""Simplified game version for Windows 7 32-bit with minimal dependencies"""
import sys
import os

# Add embedded libraries to path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

try:
    import pygame
    import random
except ImportError as e:
    print(f"Error: {e}")
    print("Please run install.bat first!")
    input("Press Enter to exit...")
    sys.exit(1)

from config import *

class SimpleGame:
    """Simplified game for low-spec systems"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Simplified player
        self.player_x = 0
        self.player_y = 0
        self.player_health = 100
        self.player_level = 1
        self.player_experience = 0
        self.camera_x = 0
        self.camera_y = 0
        
        # Game state
        self.enemies = []
        self.resources = []
        self.spawn_initial()
    
    def spawn_initial(self):
        """Spawn initial game objects"""
        # Spawn resources
        for _ in range(50):
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            self.resources.append({'x': x, 'y': y, 'type': random.choice(['stone', 'wood', 'gold'])})
        
        # Spawn enemies
        for _ in range(5):
            x = random.randint(-300, 300)
            y = random.randint(-300, 300)
            self.enemies.append({'x': x, 'y': y, 'health': 20})
    
    def handle_events(self):
        """Handle input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_y -= 5
        if keys[pygame.K_s]:
            self.player_y += 5
        if keys[pygame.K_a]:
            self.player_x -= 5
        if keys[pygame.K_d]:
            self.player_x += 5
        if keys[pygame.K_SPACE]:
            self.attack()
        if keys[pygame.K_m]:
            self.mine()
    
    def attack(self):
        """Attack nearby enemies"""
        for enemy in self.enemies[:]:
            distance = ((enemy['x'] - self.player_x)**2 + (enemy['y'] - self.player_y)**2)**0.5
            if distance < 50:
                enemy['health'] -= 10
                if enemy['health'] <= 0:
                    self.enemies.remove(enemy)
                    self.player_experience += 10
    
    def mine(self):
        """Mine nearby resources"""
        for resource in self.resources[:]:
            distance = ((resource['x'] - self.player_x)**2 + (resource['y'] - self.player_y)**2)**0.5
            if distance < 50:
                self.resources.remove(resource)
                self.player_experience += 5
    
    def update(self):
        """Update game state"""
        # Update camera
        self.camera_x = self.player_x - WINDOW_WIDTH // 2
        self.camera_y = self.player_y - WINDOW_HEIGHT // 2
        
        # Spawn new enemies
        if random.random() < 0.01 and len(self.enemies) < 10:
            x = random.randint(-300, 300) + self.player_x
            y = random.randint(-300, 300) + self.player_y
            self.enemies.append({'x': x, 'y': y, 'health': 20})
        
        # Update level
        if self.player_experience >= self.player_level * 100:
            self.player_level += 1
            self.player_health = 100
    
    def draw(self):
        """Render game"""
        self.screen.fill((40, 40, 40))
        
        # Draw grid background
        for x in range(-500, 500, 50):
            screen_x = x - self.camera_x
            pygame.draw.line(self.screen, (60, 60, 60), (screen_x, 0), (screen_x, WINDOW_HEIGHT))
        for y in range(-500, 500, 50):
            screen_y = y - self.camera_y
            pygame.draw.line(self.screen, (60, 60, 60), (0, screen_y), (WINDOW_WIDTH, screen_y))
        
        # Draw resources
        for resource in self.resources:
            screen_x = int(resource['x'] - self.camera_x)
            screen_y = int(resource['y'] - self.camera_y)
            color = {'stone': (128, 128, 128), 'wood': (139, 69, 19), 'gold': (255, 215, 0)}
            pygame.draw.circle(self.screen, color.get(resource['type'], (200, 200, 200)), (screen_x, screen_y), 5)
        
        # Draw enemies
        for enemy in self.enemies:
            screen_x = int(enemy['x'] - self.camera_x)
            screen_y = int(enemy['y'] - self.camera_y)
            pygame.draw.circle(self.screen, (255, 0, 0), (screen_x, screen_y), 8)
            
            # Enemy health bar
            health_percentage = enemy['health'] / 20
            pygame.draw.rect(self.screen, (255, 0, 0), (screen_x - 10, screen_y - 15, 20, 3))
            pygame.draw.rect(self.screen, (0, 255, 0), (screen_x - 10, screen_y - 15, 20 * health_percentage, 3))
        
        # Draw player
        screen_x = WINDOW_WIDTH // 2
        screen_y = WINDOW_HEIGHT // 2
        pygame.draw.circle(self.screen, (100, 200, 255), (screen_x, screen_y), 10)
        
        # Draw HUD
        font_small = pygame.font.Font(None, 24)
        font_large = pygame.font.Font(None, 32)
        
        health_text = font_small.render(f"Health: {self.player_health}", True, (0, 255, 0))
        level_text = font_small.render(f"Level: {self.player_level}", True, (100, 200, 255))
        exp_text = font_small.render(f"XP: {self.player_experience}/{self.player_level * 100}", True, (200, 100, 255))
        controls_text = font_small.render("WASD: Move | SPACE: Attack | M: Mine | ESC: Quit", True, (200, 200, 200))
        
        self.screen.blit(health_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(exp_text, (10, 70))
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()

if __name__ == '__main__':
    game = SimpleGame()
    game.run()
