"""Collection of mini-games and activities"""

class Fishing:
    """Fishing mini-game"""
    
    def __init__(self):
        self.active = False
        self.fish_timer = 0
        self.fish_spawn_time = 0
        self.catch_success = False
    
    def start(self):
        """Start fishing"""
        self.active = True
        self.fish_timer = 0
    
    def update(self, dt):
        """Update fishing"""
        if not self.active:
            return
        
        self.fish_timer += dt
        self.fish_spawn_time += dt
    
    def catch(self):
        """Attempt to catch fish"""
        import random
        # 50% success rate if fish is present
        if self.fish_spawn_time > 3:
            success = random.random() < 0.5
            self.active = False
            return success
        return False

class Cooking:
    """Cooking recipes"""
    
    def __init__(self):
        self.recipes = {
            'roasted_meat': {'ingredients': {'meat': 1}, 'output': 'cooked_meat', 'time': 5},
            'bread': {'ingredients': {'wheat': 3}, 'output': 'bread', 'time': 3},
            'stew': {'ingredients': {'vegetable': 2, 'meat': 1}, 'output': 'stew', 'time': 8},
        }
    
    def can_cook(self, recipe_name, inventory):
        """Check if recipe can be cooked"""
        if recipe_name not in self.recipes:
            return False
        
        recipe = self.recipes[recipe_name]
        for ingredient, quantity in recipe['ingredients'].items():
            if not inventory.has_item(ingredient, quantity):
                return False
        return True
    
    def cook(self, recipe_name, inventory):
        """Cook a recipe"""
        if not self.can_cook(recipe_name, inventory):
            return False
        
        recipe = self.recipes[recipe_name]
        for ingredient, quantity in recipe['ingredients'].items():
            inventory.remove_item(ingredient, quantity)
        
        inventory.add_item(recipe['output'], 1)
        return True

class Alchemy:
    """Alchemy potion crafting"""
    
    def __init__(self):
        self.potions = {
            'health_potion': {'ingredients': {'herb': 2}, 'effect': 'heal', 'power': 50},
            'mana_potion': {'ingredients': {'mushroom': 3}, 'effect': 'mana', 'power': 40},
            'strength_potion': {'ingredients': {'herb': 1, 'mushroom': 1}, 'effect': 'strength', 'power': 30},
        }
    
    def can_brew(self, potion_name, inventory):
        """Check if potion can be brewed"""
        if potion_name not in self.potions:
            return False
        
        potion = self.potions[potion_name]
        for ingredient, quantity in potion['ingredients'].items():
            if not inventory.has_item(ingredient, quantity):
                return False
        return True
    
    def brew(self, potion_name, inventory):
        """Brew a potion"""
        if not self.can_brew(potion_name, inventory):
            return False
        
        potion = self.potions[potion_name]
        for ingredient, quantity in potion['ingredients'].items():
            inventory.remove_item(ingredient, quantity)
        
        inventory.add_item(potion_name, 1)
        return True
