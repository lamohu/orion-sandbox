"""Skill and ability system"""

class Skill:
    """Player skill"""
    
    def __init__(self, skill_id, name, description, max_level):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.level = 0
        self.max_level = max_level
        self.experience = 0
    
    def add_experience(self, amount):
        """Add skill experience"""
        self.experience += amount
        exp_to_level = (self.level + 1) * 100
        
        while self.experience >= exp_to_level and self.level < self.max_level:
            self.experience -= exp_to_level
            self.level += 1
            exp_to_level = (self.level + 1) * 100
    
    def get_bonus(self):
        """Get bonus from skill level"""
        return 1.0 + (self.level * 0.1)

class SkillTree:
    """Player skill tree"""
    
    def __init__(self):
        self.skills = {
            'mining': Skill('mining', 'Mining', 'Increases mining speed and ore quality', 20),
            'crafting': Skill('crafting', 'Crafting', 'Increases crafting speed and quality', 20),
            'combat': Skill('combat', 'Combat', 'Increases damage and accuracy', 20),
            'defense': Skill('defense', 'Defense', 'Reduces damage taken', 20),
            'magic': Skill('magic', 'Magic', 'Increases spell damage and mana', 20),
        }
    
    def add_skill_experience(self, skill_name, amount):
        """Add experience to a skill"""
        if skill_name in self.skills:
            self.skills[skill_name].add_experience(amount)
    
    def get_skill_bonus(self, skill_name):
        """Get bonus from skill"""
        if skill_name in self.skills:
            return self.skills[skill_name].get_bonus()
        return 1.0
    
    def get_all_skills(self):
        """Get all skills"""
        return self.skills

class Ability:
    """Player ability/spell"""
    
    def __init__(self, ability_id, name, mana_cost, cooldown, damage):
        self.ability_id = ability_id
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.damage = damage
    
    def can_use(self, player):
        """Check if ability can be used"""
        return (self.current_cooldown <= 0 and 
                player.mana >= self.mana_cost)
    
    def use(self, player):
        """Use ability"""
        if self.can_use(player):
            player.mana -= self.mana_cost
            self.current_cooldown = self.cooldown
            return True
        return False
    
    def update(self, dt):
        """Update ability cooldown"""
        self.current_cooldown = max(0, self.current_cooldown - dt)
