"""World generation using Perlin noise simulation"""
import random
import math
from config import CHUNK_SIZE, BIOMES, RESOURCES, WORLD_SEED

class NoiseGenerator:
    """Simple noise generator for terrain"""
    
    def __init__(self, seed=None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.permutation = list(range(256))
        random.shuffle(self.permutation)
        self.permutation += self.permutation
    
    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, t, a, b):
        return a + t * (b - a)
    
    def _grad(self, hash_val, x, y):
        h = hash_val & 15
        u = x if h < 8 else y
        v = y if h < 8 else x
        return ((-u if (h & 1) else u) + (-2 * v if (h & 2) else 2 * v))
    
    def perlin(self, x, y):
        """Generate Perlin noise value"""
        xi = int(x) & 255
        yi = int(y) & 255
        xf = x - int(x)
        yf = y - int(y)
        
        u = self._fade(xf)
        v = self._fade(yf)
        
        p = self.permutation
        aa = p[p[xi] + yi]
        ba = p[p[xi + 1] + yi]
        ab = p[p[xi] + yi + 1]
        bb = p[p[xi + 1] + yi + 1]
        
        x1 = self._lerp(u, self._grad(aa, xf, yf), self._grad(ba, xf - 1, yf))
        x2 = self._lerp(u, self._grad(ab, xf, yf - 1), self._grad(bb, xf - 1, yf - 1))
        return (self._lerp(v, x1, x2) + 1) / 2

class Chunk:
    """Represents a chunk of the world"""
    
    def __init__(self, x, y, seed=None):
        self.x = x
        self.y = y
        self.noise = NoiseGenerator(seed)
        self.tiles = self._generate_tiles()
        self.entities = []
    
    def _generate_tiles(self):
        """Generate tiles using noise"""
        tiles = {}
        base_x = self.x * CHUNK_SIZE
        base_y = self.y * CHUNK_SIZE
        
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                world_x = base_x + i
                world_y = base_y + j
                
                # Generate biome
                biome_noise = self.noise.perlin(world_x * 0.01, world_y * 0.01)
                if biome_noise < 0.3:
                    biome = 'water'
                elif biome_noise < 0.45:
                    biome = 'snow'
                elif biome_noise < 0.6:
                    biome = 'desert'
                elif biome_noise < 0.75:
                    biome = 'plains'
                else:
                    biome = 'forest'
                
                # Generate resources
                resources = {}
                resource_noise = self.noise.perlin(world_x * 0.05, world_y * 0.05)
                
                if resource_noise > 0.85:
                    resources['stone'] = random.randint(1, 5)
                if resource_noise > 0.9:
                    resources['wood'] = random.randint(1, 3)
                if resource_noise > 0.92:
                    resources['iron'] = random.randint(1, 2)
                if resource_noise > 0.95:
                    resources['gold'] = 1
                if resource_noise > 0.98:
                    resources['diamond'] = 1
                
                tiles[(i, j)] = {
                    'biome': biome,
                    'resources': resources,
                    'world_x': world_x,
                    'world_y': world_y,
                }
        
        return tiles
    
    def get_tile(self, x, y):
        """Get tile at local coordinates"""
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE:
            return self.tiles.get((x, y))
        return None

class World:
    """Manages the world and chunks"""
    
    def __init__(self, seed=None):
        self.seed = seed or WORLD_SEED
        self.chunks = {}
        self.buildings = {}
        self.enemies = []
        self.particles = None
    
    def get_or_create_chunk(self, chunk_x, chunk_y):
        """Get chunk or create if it doesn't exist"""
        key = (chunk_x, chunk_y)
        if key not in self.chunks:
            self.chunks[key] = Chunk(chunk_x, chunk_y, self.seed)
        return self.chunks[key]
    
    def get_tile_at_world_pos(self, world_x, world_y):
        """Get tile at world coordinates"""
        chunk_x = world_x // CHUNK_SIZE
        chunk_y = world_y // CHUNK_SIZE
        local_x = world_x % CHUNK_SIZE
        local_y = world_y % CHUNK_SIZE
        
        chunk = self.get_or_create_chunk(chunk_x, chunk_y)
        return chunk.get_tile(local_x, local_y)
    
    def get_chunks_in_view(self, camera_x, camera_y, view_width, view_height):
        """Get all chunks visible in camera view"""
        chunk_x = camera_x // CHUNK_SIZE
        chunk_y = camera_y // CHUNK_SIZE
        chunks_x = (view_width // CHUNK_SIZE) + 2
        chunks_y = (view_height // CHUNK_SIZE) + 2
        
        visible_chunks = []
        for dx in range(-1, chunks_x + 1):
            for dy in range(-1, chunks_y + 1):
                cx = chunk_x + dx
                cy = chunk_y + dy
                visible_chunks.append(self.get_or_create_chunk(cx, cy))
        
        return visible_chunks
    
    def place_building(self, x, y, building_type):
        """Place a building at world coordinates"""
        self.buildings[(x, y)] = building_type
    
    def get_building_at(self, x, y):
        """Get building at coordinates"""
        return self.buildings.get((x, y))
    
    def remove_building(self, x, y):
        """Remove building at coordinates"""
        if (x, y) in self.buildings:
            del self.buildings[(x, y)]
    
    def update(self, dt):
        """Update world state"""
        pass
