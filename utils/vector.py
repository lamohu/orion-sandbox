import math

class Vector2:
    """2D Vector class for positions and velocities"""
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return Vector2(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return Vector2(self.x - other, self.y - other)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def distance_to(self, other):
        return (self - other).magnitude()
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def angle_to(self, other):
        diff = other - self
        return math.atan2(diff.y, diff.x)
    
    def to_tuple(self):
        return (int(self.x), int(self.y))
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
