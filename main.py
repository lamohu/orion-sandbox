"""Complete game implementation with all systems integrated"""
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
from systems.loot import LootSystem
from systems.npc import NPCManager, NPC
from systems.progression import QuestSystem, ProgressionSystem
from systems.boss import BossArena, BossAI, BossReward
from systems.effects import EffectSystem
from systems.world_systems import DayNightCycle, ResourceSpawner, DifficultyScaler
from systems.input import InputHandler
from systems.debug import DebugDisplay
from systems.save_system import SaveManager
from systems.skills import SkillTree
from systems.enchantment import EnchantmentSystem
from systems.activities import Cooking, Alchemy
from ui.hud import HUD, InventoryUI, CraftingUI, BuildingUI, PauseMenu
from ui.enhanced_ui import QuestLogUI
from utils.vector import Vector2

class Game:
    """Complete game implementation"""
    
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
        self.player.mana = 100
        self.player.max_mana = 100
        
        self.crafting_system = CraftingSystem(CRAFTING_RECIPES)
        self.combat_system = CombatSystem()
        self.building_system = BuildingSystem()
        self.mining_system = MiningSystem()
        self.loot_system = LootSystem()
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.npc_manager = NPCManager()
        self.quest_system = QuestSystem()
        self.progression_system = ProgressionSystem()
        self.effect_system = EffectSystem()
        self.day_night_cycle = DayNightCycle()
        self.resource_spawner = ResourceSpawner(self.mining_system)
        self.difficulty_scaler = DifficultyScaler()
        self.skill_tree = SkillTree()
        self.enchantment_system = EnchantmentSystem()
        self.cooking = Cooking()
        self.alchemy = Alchemy()
        self.input_handler = InputHandler()
        self.debug_display = DebugDisplay()
        self.save_manager = SaveManager()
        
        # UI
        self.hud = HUD(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.inventory_ui = InventoryUI(50, 200, 300, 400)
        self.crafting_ui = CraftingUI(WINDOW_WIDTH - 350, 200, 300, 400)
        self.building_ui = BuildingUI(WINDOW_WIDTH - 350, 50, 300, 150)
        self.quest_log_ui = QuestLogUI(50, 50, 300, 150)
        self.pause_menu = PauseMenu(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Toggle states
        self.show_inventory = False
        self.show_crafting = False
        self.show_building = False
        self.show_quest_log = False
        
        # Entities
        self.enemies = []
        self.bosses = []
        self.boss_arenas = []
        
        # Initialize game
        self.spawn_enemies()
        self.spawn_bosses()
        self.generate_resources()
        self.setup_npcs()
        self.setup_quests()
    
    def generate_resources(self):
        """Generate resource nodes"""
        for _ in range(200):
            x = random.randint(-500, 500)
            y = random.randint(-500, 500)
            resource_type = random.choice(['stone', 'wood', 'iron', 'gold', 'diamond'])
            self.mining_system.add_resource(x, y, resource_type)
    
    def spawn_enemies(self):
        """Spawn enemies"""
        for _ in range(10):
            x = random.randint(-300, 300)
            y = random.randint(-300, 300)
            enemy_type = random.choice(list(ENEMY_TYPES.keys()))
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def spawn_bosses(self):
        """Spawn bosses with arenas"""
        boss_positions = [(500, 500), (-500, 500), (500, -500), (-500, -500)]
        for pos in boss_positions:
            boss_type = random.choice(list(BOSSES.keys()))
            boss = Boss(pos[0], pos[1], boss_type)
            self.bosses.append(boss)
            arena = BossArena(pos[0], pos[1], 300)
            self.boss_arenas.append(arena)
    
    def setup_npcs(self):
        """Setup NPCs in world"""
        npc_data = [
            ('merchant', 'Merchant', 100, 100, ['Hello traveler!', 'Welcome to my shop!', 'Anything else?']),
            ('guard', 'Guard', -100, 100, ['Stay safe!', 'Watch out for monsters!', 'Good luck!']),
        ]
        
        for npc_id, name, x, y, dialogue in npc_data:
            npc = NPC(npc_id, name, x, y, dialogue)
            self.npc_manager.add_npc(npc_id, npc)
    
    def setup_quests(self):
        """Setup initial quests"""
        self.quest_system.add_quest('gather_wood')
        self.quest_system.add_quest('gather_stone')
    
    def handle_events(self):
        """Handle events"""
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
                    elif event.key == pygame.K_q:
                        self.show_quest_log = not self.show_quest_log
                    elif event.key == pygame.K_F3:
                        self.debug_display.toggle()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.paused and event.button == 1:
                    # Left click to place building
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
        
        # Input
        self.input_handler.update()
        movement = self.input_handler.get_movement_vector()
        from utils.vector import Vector2
        self.player.vel = Vector2(movement[0], movement[1]) * PLAYER_SPEED
        
        # Update systems
        self.player.update(dt, self.world, self.camera)
        self.camera.update(dt)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.world, self.player)
        
        # Update bosses
        for i, boss in enumerate(self.bosses):
            arena = self.boss_arenas[i]
            arena.enter_arena(self.player, boss)
            boss.update(dt, self.world, self.player)
        
        # Remove dead
        self.enemies = [e for e in self.enemies if e.alive]
        self.bosses = [b for b in self.bosses if b.alive]
        
        # Mining
        if self.input_handler.is_key_pressed('mining'):
            harvested = self.mining_system.mine_nearby(self.player, 5)
            for resource_type, amount in harvested.items():
                self.player.inventory.add_item(resource_type, amount)
                self.effect_system.spawn_damage_effect(self.player.pos.x, self.player.pos.y)
        
        # Combat
        if self.input_handler.is_key_pressed('attack'):
            self.player.attack(self.enemies + self.bosses)
        
        # Pick up loot
        self.loot_system.pickup_nearby(self.player)
        
        # Update systems
        self.building_system.update(dt)
        self.loot_system.update(dt)
        self.effect_system.update(dt)
        self.day_night_cycle.update(dt)
        self.resource_spawner.update(dt, self.player)
        self.difficulty_scaler.update(self.player.level)
        self.debug_display.update(dt)
        
        # Spawn new enemies
        if random.random() < 0.001:
            x = random.randint(-300, 300) + self.player.pos.x
            y = random.randint(-300, 300) + self.player.pos.y
            enemy_type = random.choice(list(ENEMY_TYPES.keys()))
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def draw(self):
        """Render game"""
        self.screen.fill((40, 40, 40))
        offset = self.camera.get_offset()
        
        # Draw world
        self.draw_world(offset)
        self.building_system.draw(self.screen, offset)
        self.mining_system.draw(self.screen, offset)
        self.loot_system.draw(self.screen, offset)
        
        # Draw entities
        for enemy in self.enemies:
            enemy.draw(self.screen, offset)
        for boss in self.bosses:
            boss.draw(self.screen, offset)
        
        # Draw bosses arenas
        for arena in self.boss_arenas:
            arena.draw(self.screen, offset)
        
        # Draw NPCs
        self.npc_manager.draw(self.screen, offset)
        
        # Draw player
        self.player.draw(self.screen, offset)
        
        # Draw effects
        self.effect_system.draw(self.screen, offset)
        
        # Draw UI
        self.hud.draw(self.screen, self.player)
        
        self.inventory_ui.visible = self.show_inventory
        self.crafting_ui.visible = self.show_crafting
        self.building_ui.visible = self.show_building
        self.quest_log_ui.visible = self.show_quest_log
        
        if self.show_inventory:
            self.inventory_ui.draw(self.screen, self.player)
        if self.show_crafting:
            available = self.crafting_system.get_available_recipes(self.player.inventory)
            self.crafting_ui.draw(self.screen, available)
        if self.show_building:
            self.building_ui.draw(self.screen)
        if self.show_quest_log:
            self.quest_log_ui.draw(self.screen, self.quest_system)
        
        if self.paused:
            self.pause_menu.draw(self.screen)
        
        # Draw debug info
        self.debug_display.draw(self.screen, self)
        
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
