"""Resource and mining system"""
from config import RESOURCES

class ResourceNode:
    """A gatherable resource in the world"""
    
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.max_health = 10
        self.health = 10
        self.harvest_amount = 1
    
    def mine(self, damage=1):
        """Mine the resource node"""
        self.health -= damage
        if self.health <= 0:
            return self.harvest_amount
        return 0
    
    def draw(self, surface, camera_offset):
        """Draw resource node"""
        import pygame
        if self.resource_type in RESOURCES:
            color = RESOURCES[self.resource_type]['color']
            screen_x = int(self.x - camera_offset.x)
            screen_y = int(self.y - camera_offset.y)
            pygame.draw.circle(surface, color, (screen_x, screen_y), 8)

class MiningSystem:
    """Handles mining mechanics"""
    
    def __init__(self):
        self.resource_nodes = []
    
    def add_resource(self, x, y, resource_type):
        """Add a resource node"""
        node = ResourceNode(x, y, resource_type)
        self.resource_nodes.append(node)
    
    def mine_nearby(self, player, mining_damage):
        """Mine resources near player"""
        mining_range = 50
        harvested = {}
        
        for node in self.resource_nodes:
            distance = player.pos.distance_to((node.x, node.y))
            if distance < mining_range:
                amount = node.mine(mining_damage)
                if amount > 0:
                    if node.resource_type not in harvested:
                        harvested[node.resource_type] = 0
                    harvested[node.resource_type] += amount
        
        # Remove dead nodes
        self.resource_nodes = [n for n in self.resource_nodes if n.health > 0]
        
        return harvested
    
    def draw(self, surface, camera_offset):
        """Draw all resource nodes"""
        for node in self.resource_nodes:
            node.draw(surface, camera_offset)
    
    def get_nearby_resources(self, x, y, range_dist):
        """Get resources near a position"""
        nearby = []
        for node in self.resource_nodes:
            distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
            if distance < range_dist:
                nearby.append(node)
        return nearby
