"""Debug and utility features"""
import pygame

class DebugDisplay:
    """Debug information display"""
    
    def __init__(self, font_size=16):
        self.font = pygame.font.Font(None, font_size)
        self.enabled = False
        self.fps = 0
        self.frame_count = 0
        self.time_accumulator = 0
    
    def update(self, dt):
        """Update debug info"""
        self.frame_count += 1
        self.time_accumulator += dt
        
        if self.time_accumulator >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.time_accumulator = 0
    
    def draw(self, surface, game=None):
        """Draw debug information"""
        if not self.enabled:
            return
        
        y_offset = 10
        debug_info = [
            f"FPS: {self.fps}",
            f"Position: {int(game.player.pos.x)}, {int(game.player.pos.y)}" if game else "",
            f"Enemies: {len(game.enemies)}" if game else "",
            f"Buildings: {len(game.building_system.buildings)}" if game else "",
        ]
        
        for info in debug_info:
            if info:
                text_surface = self.font.render(info, True, (0, 255, 0))
                surface.blit(text_surface, (10, y_offset))
                y_offset += 20
    
    def toggle(self):
        """Toggle debug display"""
        self.enabled = not self.enabled

class CheatCodeHandler:
    """Handle cheat codes"""
    
    def __init__(self):
        self.cheat_codes = {
            'godmode': self._godmode,
            'addexp': self._add_experience,
            'addgold': self._add_gold,
            'levelup': self._level_up,
            'spawnboss': self._spawn_boss,
        }
    
    def execute(self, code, game):
        """Execute a cheat code"""
        if code in self.cheat_codes:
            self.cheat_codes[code](game)
            return True
        return False
    
    def _godmode(self, game):
        """Enable god mode"""
        game.player.health = game.player.max_health * 100
    
    def _add_experience(self, game):
        """Add 1000 experience"""
        game.player.gain_experience(1000)
    
    def _add_gold(self, game):
        """Add gold"""
        game.player.inventory.add_item('gold', 100)
    
    def _level_up(self, game):
        """Level up player"""
        game.player.level_up()
    
    def _spawn_boss(self, game):
        """Spawn a random boss"""
        import random
        from entities.enemy import Boss
        from config import BOSSES
        
        boss_type = random.choice(list(BOSSES.keys()))
        boss = Boss(game.player.pos.x + 100, game.player.pos.y, boss_type)
        game.bosses.append(boss)
