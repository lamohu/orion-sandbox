"""Combat system"""
import random
import math

class CombatSystem:
    """Handles combat mechanics"""
    
    def __init__(self):
        self.active_fights = []
    
    def calculate_damage(self, attacker, defender, weapon=None):
        """Calculate damage based on stats"""
        base_damage = attacker.attack_damage
        
        # Weapon bonuses
        if weapon:
            from config import ITEM_STATS
            if weapon in ITEM_STATS:
                base_damage += ITEM_STATS[weapon].get('damage', 0)
        
        # Add some variance
        variance = random.uniform(0.8, 1.2)
        final_damage = base_damage * variance
        
        return int(final_damage)
    
    def check_hit(self, attacker, defender, range_distance):
        """Check if attack hits"""
        distance = attacker.distance_to(defender)
        if distance > range_distance:
            return False
        
        # 90% hit chance
        return random.random() < 0.9
    
    def apply_knockback(self, entity, direction, force):
        """Apply knockback to entity"""
        entity.vel = direction.normalize() * force
    
    def update(self, dt, entities):
        """Update combat state"""
        pass
