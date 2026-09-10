"""Main game engine"""
import pygame
import sys
import random
from config import *
from world.world import World
from entities.player import Player
from entities.enemy import Enemy, Boss
from systems.crafting import CraftingSystem
from systems.combat import CombatSystem
from systems.building import BuildingSystem
from systems.mining import MiningSystem
from systems.camera import Camera
from ui.hud import HUD, InventoryUI, CraftingUI, BuildingUI, PauseMenu
from utils.vector import Vector2

class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Game systems
        self.world = World(WORLD_SEED)
        self.player = Player(0, 0)
        self.crafting_system = CraftingSystem(CRAFTING_RECIPES)
        self.combat_system = CombatSystem()
        self.building_system = BuildingSystem()
        self.mining_system = MiningSystem()
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # UI
        self.hud = HUD(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.inventory_ui = InventoryUI(50, 200, 300, 400)
        self.crafting_ui = CraftingUI(WINDOW_WIDTH - 350, 200, 300, 400)
        self.building_ui = BuildingUI(WINDOW_WIDTH - 350, 50, 300, 150)
        self.pause_menu = PauseMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Toggle states
        self.show_inventory = False
        self.show_crafting = False
        self.show_building = False
        
        # Enemies and bosses
        self.enemies = []
        self.bosses = []
        self.spawn_enemies()
        self.spawn_bosses()
        
        # Generate initial resources
        self.generate_resources()
    
    def generate_resources(self):
        """Generate resource nodes in the world"""
        for _ in range(200):
            x = random.randint(-500, 500)
            y = random.randint(-500, 500)
            resource_type = random.choice(['stone', 'wood', 'iron', 'gold', 'diamond'])
            self.mining_system.add_resource(x, y, resource_type)
    
    def spawn_enemies(self):
        """Spawn initial enemies"""
        for _ in range(10):
            x = random.randint(-300, 300)
            y = random.randint(-300, 300)
            enemy_type = random.choice(list(ENEMY_TYPES.keys()))
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def spawn_bosses(self):
        """Spawn bosses"""
        boss_type = random.choice(list(BOSSES.keys()))
        boss = Boss(500, 500, boss_type)
        self.bosses.append(boss)
    
    def handle_events(self):
        """Handle user input and events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                
                elif not self.paused:
                    if event.key == pygame.K_e:
                        self.show_inventory = not self.show_inventory
                    elif event.key == pygame.K_c:
                        self.show_crafting = not self.show_crafting
                    elif event.key == pygame.K_b:
                        self.show_building = not self.show_building
                    elif event.key == pygame.K_SPACE:
                        self.player.attack(self.enemies + self.bosses)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.paused and event.button == 1:  # Left click
                    # Try to place building
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    offset = self.camera.get_offset()
                    world_x = mouse_x + offset.x
                    world_y = mouse_y + offset.y
                    
                    if self.building_ui.selected_building:
                        self.building_system.place_building(
                            int(world_x), int(world_y), 
                            self.building_ui.selected_building, 
                            self.player.inventory
                        )
    
    def update(self, dt):
        """Update game state"""
        if self.paused:
            return
        
        # Handle input
        keys = {
            'w': pygame.key.get_pressed()[pygame.K_w],
            'a': pygame.key.get_pressed()[pygame.K_a],
            's': pygame.key.get_pressed()[pygame.K_s],
            'd': pygame.key.get_pressed()[pygame.K_d],
        }
        self.player.handle_input(keys)
        
        # Update player
        self.player.update(dt, self.world, self.camera)
        
        # Update camera
        self.camera.update(dt)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.world, self.player)
        
        # Update bosses
        for boss in self.bosses:
            boss.update(dt, self.world, self.player)
        
        # Remove dead enemies and bosses
        self.enemies = [e for e in self.enemies if e.alive]
        self.bosses = [b for b in self.bosses if b.alive]
        
        # Mining
        if pygame.key.get_pressed()[pygame.K_m]:
            harvested = self.mining_system.mine_nearby(self.player, 5)
            for resource_type, amount in harvested.items():
                self.player.inventory.add_item(resource_type, amount)
        
        # Update buildings
        self.building_system.update(dt)
        
        # Spawn new enemies occasionally
        if random.random() < 0.001:
            x = random.randint(-300, 300)
            y = random.randint(-300, 300)
            enemy_type = random.choice(list(ENEMY_TYPES.keys()))
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def draw(self):
        """Render game"""
        self.screen.fill((40, 40, 40))
        
        offset = self.camera.get_offset()
        
        # Draw world
        self.draw_world(offset)
        
        # Draw buildings
        self.building_system.draw(self.screen, offset)
        
        # Draw resources
        self.mining_system.draw(self.screen, offset)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, offset)
        
        # Draw bosses
        for boss in self.bosses:
            boss.draw(self.screen, offset)
        
        # Draw player
        self.player.draw(self.screen, offset)
        
        # Draw HUD
        self.hud.draw(self.screen, self.player)
        
        # Draw UI panels
        self.inventory_ui.visible = self.show_inventory
        self.crafting_ui.visible = self.show_crafting
        self.building_ui.visible = self.show_building
        
        if self.show_inventory:
            self.inventory_ui.draw(self.screen, self.player)
        
        if self.show_crafting:
            available = self.crafting_system.get_available_recipes(self.player.inventory)
            self.crafting_ui.draw(self.screen, available)
        
        if self.show_building:
            self.building_ui.draw(self.screen)
        
        if self.paused:
            self.pause_menu.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_world(self, offset):
        """Draw world tiles"""
        chunks = self.world.get_chunks_in_view(
            offset.x, offset.y, 
            WINDOW_WIDTH, WINDOW_HEIGHT
        )
        
        for chunk in chunks:
            for (local_x, local_y), tile in chunk.tiles.items():
                world_x = chunk.x * CHUNK_SIZE + local_x
                world_y = chunk.y * CHUNK_SIZE + local_y
                
                screen_x = world_x * TILE_SIZE - offset.x
                screen_y = world_y * TILE_SIZE - offset.y
                
                # Draw tile
                color = BIOMES[tile['biome']]['color']
                pygame.draw.rect(self.screen, color, 
                               (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, (100, 100, 100), 
                               (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
