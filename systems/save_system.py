"""Save and load game state"""
import json
import os
from datetime import datetime

class SaveManager:
    """Manages game saves"""
    
    def __init__(self, save_dir='saves'):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, player, world, filename=None):
        """Save game state"""
        if filename is None:
            filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        save_data = {
            'player': {
                'x': player.pos.x,
                'y': player.pos.y,
                'health': player.health,
                'level': player.level,
                'experience': player.experience,
                'hunger': player.hunger,
                'inventory': self._serialize_inventory(player.inventory),
            },
            'world': {
                'seed': world.seed,
                'buildings': self._serialize_buildings(world.buildings),
            },
            'timestamp': datetime.now().isoformat(),
        }
        
        filepath = os.path.join(self.save_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return filepath
    
    def load_game(self, filename):
        """Load game state"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            save_data = json.load(f)
        
        return save_data
    
    def get_saves(self):
        """Get list of available saves"""
        saves = []
        for file in os.listdir(self.save_dir):
            if file.endswith('.json'):
                saves.append(file)
        return sorted(saves, reverse=True)
    
    def _serialize_inventory(self, inventory):
        """Convert inventory to JSON-serializable format"""
        inv_data = {}
        for item_type, item in inventory.items.items():
            inv_data[item_type] = item.quantity
        return inv_data
    
    def _serialize_buildings(self, buildings):
        """Convert buildings to JSON-serializable format"""
        buildings_data = []
        for (x, y), building in buildings.items():
            buildings_data.append({
                'x': x,
                'y': y,
                'type': building.building_type,
                'health': building.health,
            })
        return buildings_data

class GameSettings:
    """Game settings"""
    
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        
        # Default settings
        return {
            'volume': 0.8,
            'difficulty': 'normal',
            'graphics_quality': 'high',
            'show_fps': True,
            'show_grid': False,
        }
    
    def save_settings(self):
        """Save settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
