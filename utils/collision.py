import math
from utils.vector import Vector2

class Rect:
    """Rectangle for collision detection"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def collides_with(self, other):
        """Check if this rectangle collides with another"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
    
    def contains_point(self, x, y):
        """Check if a point is inside this rectangle"""
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)
    
    def distance_to_point(self, x, y):
        """Get distance from rectangle to a point"""
        dx = max(self.x - x, 0, x - (self.x + self.width))
        dy = max(self.y - y, 0, y - (self.y + self.height))
        return math.sqrt(dx * dx + dy * dy)

class CircleCollider:
    """Circle collider for entities"""
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def collides_with_circle(self, other):
        """Check collision with another circle"""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < self.radius + other.radius
    
    def collides_with_rect(self, rect):
        """Check collision with a rectangle"""
        closest_x = max(rect.x, min(self.x, rect.x + rect.width))
        closest_y = max(rect.y, min(self.y, rect.y + rect.height))
        distance = math.sqrt((self.x - closest_x) ** 2 + (self.y - closest_y) ** 2)
        return distance < self.radius
    
    def update_position(self, x, y):
        self.x = x
        self.y = y
