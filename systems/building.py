"""Building and construction system"""
from config import BUILDINGS
from utils.collision import Rect

class Building:
    """Represents a placed building"""
    
    def __init__(self, x, y, building_type):
        self.x = x
        self.y = y
        self.building_type = building_type
        config = BUILDINGS[building_type]
        self.max_health = config['hp']
        self.health = config['hp']
        self.size = config['size']
        self.cost = config['cost']
        self.collider = Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        return self.health > 0
    
    def update_collider(self):
        """Update collision box"""
        self.collider = Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def draw(self, surface, camera_offset):
        """Draw building"""
        import pygame
        screen_x = int(self.x - camera_offset.x)
        screen_y = int(self.y - camera_offset.y)
        
        # Draw building
        color = {
            'wall': (128, 128, 128),
            'door': (139, 69, 19),
            'chest': (184, 134, 11),
            'campfire': (255, 100, 0),
            'tower': (100, 100, 100),
        }.get(self.building_type, (200, 200, 200))
        
        pygame.draw.rect(surface, color, 
                         (screen_x - self.size // 2, screen_y - self.size // 2, self.size, self.size))
        
        # Draw health bar
        health_percentage = self.health / self.max_health
        bar_width = self.size
        pygame.draw.rect(surface, (255, 0, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 8, bar_width, 3))
        pygame.draw.rect(surface, (0, 255, 0), 
                         (screen_x - bar_width // 2, screen_y - self.size // 2 - 8, 
                          bar_width * health_percentage, 3))

class BuildingSystem:
    """Manages building placement and destruction"""
    
    def __init__(self):
        self.buildings = {}  # (x, y): Building
    
    def can_place_building(self, x, y, building_type, player_inventory):
        """Check if building can be placed"""
        # Check if position is empty
        if (x, y) in self.buildings:
            return False, "Space occupied"
        
        # Check if player has materials
        building_config = BUILDINGS[building_type]
        for material, quantity in building_config['cost'].items():
            if not player_inventory.has_item(material, quantity):
                return False, f"Need {quantity} {material}"
        
        return True, "OK"
    
    def place_building(self, x, y, building_type, player_inventory):
        """Place a building"""
        can_place, msg = self.can_place_building(x, y, building_type, player_inventory)
        if not can_place:
            return False
        
        # Consume materials
        building_config = BUILDINGS[building_type]
        for material, quantity in building_config['cost'].items():
            player_inventory.remove_item(material, quantity)
        
        # Place building
        building = Building(x, y, building_type)
        self.buildings[(x, y)] = building
        return True
    
    def get_building_at(self, x, y, range_dist=50):
        """Get building near coordinates"""
        for (bx, by), building in self.buildings.items():
            if abs(bx - x) < range_dist and abs(by - y) < range_dist:
                return building
        return None
    
    def destroy_building(self, x, y):
        """Destroy building at coordinates"""
        if (x, y) in self.buildings:
            del self.buildings[(x, y)]
            return True
        return False
    
    def update(self, dt):
        """Update buildings"""
        to_remove = []
        for pos, building in self.buildings.items():
            if building.health <= 0:
                to_remove.append(pos)
        
        for pos in to_remove:
            del self.buildings[pos]
    
    def draw(self, surface, camera_offset):
        """Draw all buildings"""
        for building in self.buildings.values():
            building.draw(surface, camera_offset)
