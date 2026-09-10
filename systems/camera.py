"""Camera system"""
from utils.vector import Vector2

class Camera:
    """Game camera"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = Vector2(0, 0)
        self.target = Vector2(0, 0)
        self.zoom = 1.0
    
    def update(self, dt):
        """Update camera position with smooth follow"""
        # Smooth follow target
        follow_speed = 5
        diff = self.target - self.pos
        if diff.magnitude() > 0.1:
            self.pos = self.pos + diff.normalize() * follow_speed * dt
        else:
            self.pos = self.target.copy()
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return Vector2(self.pos.x - self.width // 2, self.pos.y - self.height // 2)
    
    def world_to_screen(self, world_pos, offset):
        """Convert world position to screen position"""
        return Vector2(world_pos.x - offset.x, world_pos.y - offset.y)
    
    def screen_to_world(self, screen_pos, offset):
        """Convert screen position to world position"""
        return Vector2(screen_pos.x + offset.x, screen_pos.y + offset.y)
