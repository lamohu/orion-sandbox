"""Advanced world features and mechanics"""
import random
import math

class WeatherSystem:
    """Weather affects gameplay"""
    
    def __init__(self):
        self.weather_type = 'clear'
        self.weather_timer = 0
        self.weather_duration = random.uniform(30, 120)
    
    def update(self, dt):
        """Update weather"""
        self.weather_timer += dt
        
        if self.weather_timer >= self.weather_duration:
            self.weather_timer = 0
            self.weather_duration = random.uniform(30, 120)
            
            weather_types = ['clear', 'rain', 'storm']
            self.weather_type = random.choice(weather_types)
    
    def get_weather_effect(self):
        """Get effect of current weather"""
        effects = {
            'clear': {'speed_bonus': 1.0, 'vision': 1.0},
            'rain': {'speed_bonus': 0.8, 'vision': 0.8},
            'storm': {'speed_bonus': 0.6, 'vision': 0.5},
        }
        return effects.get(self.weather_type, {'speed_bonus': 1.0, 'vision': 1.0})

class DayNightCycle:
    """Day/night cycle affects enemy spawning"""
    
    def __init__(self):
        self.time = 0
        self.cycle_duration = 300  # 5 minutes = 1 day/night cycle
    
    def update(self, dt):
        """Update time"""
        self.time += dt
        self.time = self.time % self.cycle_duration
    
    def is_night(self):
        """Check if it's night"""
        return self.time > self.cycle_duration / 2
    
    def get_brightness(self):
        """Get brightness level (0-1)"""
        if self.is_night():
            return 0.4
        return 1.0

class ResourceSpawner:
    """Spawns resources dynamically"""
    
    def __init__(self, mining_system):
        self.mining_system = mining_system
        self.spawn_timer = 0
        self.spawn_interval = 10  # Spawn every 10 seconds
    
    def update(self, dt, player):
        """Update resource spawning"""
        self.spawn_timer += dt
        
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            
            # Spawn resources around player
            for _ in range(random.randint(1, 3)):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(200, 400)
                x = player.pos.x + math.cos(angle) * distance
                y = player.pos.y + math.sin(angle) * distance
                
                resource_type = random.choice(['stone', 'wood', 'iron', 'gold', 'diamond'])
                self.mining_system.add_resource(x, y, resource_type)

class DifficultyScaler:
    """Scales difficulty based on player level"""
    
    def __init__(self):
        self.difficulty = 1.0
    
    def update(self, player_level):
        """Update difficulty scaling"""
        self.difficulty = 1.0 + (player_level - 1) * 0.1
    
    def get_enemy_health_multiplier(self):
        return self.difficulty
    
    def get_enemy_damage_multiplier(self):
        return self.difficulty * 0.8
    
    def get_boss_health_multiplier(self):
        return self.difficulty * 1.5
