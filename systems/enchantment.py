"""Item enchantment and upgrade system"""
import random

class Enchantment:
    """Item enchantment"""
    
    def __init__(self, enchant_id, name, effect_type, power):
        self.enchant_id = enchant_id
        self.name = name
        self.effect_type = effect_type  # damage, defense, speed, etc.
        self.power = power
    
    def get_bonus(self):
        """Get bonus from enchantment"""
        return self.power * 0.1

class EnchantedItem:
    """Item with enchantments"""
    
    def __init__(self, item_type, enchantments=None):
        self.item_type = item_type
        self.enchantments = enchantments or []
        self.level = 1
        self.durability = 100
        self.max_durability = 100
    
    def add_enchantment(self, enchantment):
        """Add enchantment to item"""
        if len(self.enchantments) < 3:  # Max 3 enchantments
            self.enchantments.append(enchantment)
            return True
        return False
    
    def get_total_bonus(self, effect_type):
        """Get total bonus for effect type"""
        total = 0
        for enchant in self.enchantments:
            if enchant.effect_type == effect_type:
                total += enchant.get_bonus()
        return total
    
    def use(self):
        """Use item (reduces durability)"""
        self.durability = max(0, self.durability - 1)
    
    def repair(self, amount):
        """Repair item"""
        self.durability = min(self.durability + amount, self.max_durability)
    
    def upgrade(self):
        """Upgrade item level"""
        self.level += 1
        self.max_durability += 10
        self.durability = self.max_durability

class EnchantmentSystem:
    """Manages item enchantments"""
    
    def __init__(self):
        self.available_enchantments = {
            'sharpness': Enchantment('sharpness', 'Sharpness', 'damage', 3),
            'protection': Enchantment('protection', 'Protection', 'defense', 2),
            'speed': Enchantment('speed', 'Speed', 'speed', 2),
            'fortune': Enchantment('fortune', 'Fortune', 'luck', 2),
            'efficiency': Enchantment('efficiency', 'Efficiency', 'speed', 3),
        }
        self.enchantment_cost = 50  # Gold cost to enchant
    
    def enchant_item(self, item, enchantment_name, player):
        """Enchant an item"""
        if enchantment_name not in self.available_enchantments:
            return False
        
        if not player.inventory.has_item('gold', self.enchantment_cost):
            return False
        
        enchant = self.available_enchantments[enchantment_name]
        if isinstance(item, EnchantedItem):
            if item.add_enchantment(enchant):
                player.inventory.remove_item('gold', self.enchantment_cost)
                return True
        
        return False
    
    def upgrade_item(self, item, player):
        """Upgrade an item"""
        upgrade_cost = item.level * 100
        if player.inventory.has_item('gold', upgrade_cost):
            item.upgrade()
            player.inventory.remove_item('gold', upgrade_cost)
            return True
        return False

class ItemRarity:
    """Item rarity levels"""
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
