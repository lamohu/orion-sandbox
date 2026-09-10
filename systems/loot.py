"""Loot and drop system"""
import random
from config import RESOURCES

class LootTable:
    """Defines loot drop tables"""
    
    def __init__(self):
        self.tables = {
            'goblin': {'gold': (1, 5), 'wood': (0, 3)},
            'skeleton': {'gold': (5, 15), 'iron': (1, 3)},
            'zombie': {'gold': (3, 10), 'stone': (2, 5)},
            'fire_elemental': {'diamond': (2, 5), 'gold': (10, 20), 'iron': (10, 15)},
            'ice_golem': {'diamond': (1, 3), 'gold': (8, 15), 'iron': (8, 12)},
            'dark_lord': {'diamond': (5, 10), 'gold': (20, 30), 'iron': (15, 25)},
        }
    
    def get_loot(self, entity_type):
        """Generate loot from entity"""
        if entity_type not in self.tables:
            return {}
        
        loot = {}
        table = self.tables[entity_type]
        
        for item, quantity_range in table.items():
            if random.random() < 0.8:  # 80% drop chance
                loot[item] = random.randint(quantity_range[0], quantity_range[1])
        
        return loot

class ItemDrop:
    """A dropped item in the world"""
    
    def __init__(self, x, y, item_type, quantity):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.quantity = quantity
        self.pickup_range = 30
        self.age = 0
        self.lifetime = 300  # 5 minutes
    
    def update(self, dt):
        """Update item drop"""
        self.age += dt
    
    def is_alive(self):
        """Check if item still exists"""
        return self.age < self.lifetime
    
    def can_pickup(self, player_pos):
        """Check if player can pick up item"""
        distance = ((player_pos.x - self.x) ** 2 + (player_pos.y - self.y) ** 2) ** 0.5
        return distance < self.pickup_range
    
    def draw(self, surface, camera_offset):
        """Draw item drop"""
        import pygame
        if self.item_type in RESOURCES:
            color = RESOURCES[self.item_type]['color']
            screen_x = int(self.x - camera_offset.x)
            screen_y = int(self.y - camera_offset.y)
            pygame.draw.rect(surface, color, (screen_x - 5, screen_y - 5, 10, 10))
            pygame.draw.rect(surface, (255, 255, 255), (screen_x - 5, screen_y - 5, 10, 10), 1)

class LootSystem:
    """Manages loot drops"""
    
    def __init__(self):
        self.loot_table = LootTable()
        self.drops = []
    
    def create_drop(self, x, y, entity_type):
        """Create loot drops from defeated entity"""
        loot = self.loot_table.get_loot(entity_type)
        
        for item_type, quantity in loot.items():
            # Spread loot around slightly
            import random
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            drop = ItemDrop(x + offset_x, y + offset_y, item_type, quantity)
            self.drops.append(drop)
    
    def update(self, dt):
        """Update loot drops"""
        for drop in self.drops:
            drop.update(dt)
        
        self.drops = [d for d in self.drops if d.is_alive()]
    
    def pickup_nearby(self, player):
        """Pick up nearby loot"""
        for drop in self.drops:
            if drop.can_pickup(player.pos):
                player.inventory.add_item(drop.item_type, drop.quantity)
                self.drops.remove(drop)
    
    def draw(self, surface, camera_offset):
        """Draw all loot drops"""
        for drop in self.drops:
            drop.draw(surface, camera_offset)
