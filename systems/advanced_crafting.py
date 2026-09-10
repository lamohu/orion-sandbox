"""Advanced crafting and recipe system"""

class RecipeCategory:
    """Category of recipes"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.recipes = []
    
    def add_recipe(self, recipe_name):
        """Add recipe to category"""
        self.recipes.append(recipe_name)

class AdvancedRecipe:
    """Advanced crafting recipe"""
    
    def __init__(self, recipe_id, name, ingredients, output, quantity, time, requirements=None):
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients
        self.output = output
        self.quantity = quantity
        self.time = time
        self.requirements = requirements or {}  # Level, tools, etc.
        self.description = ""
    
    def can_craft(self, player, inventory):
        """Check if recipe can be crafted"""
        # Check ingredients
        for ingredient, quantity in self.ingredients.items():
            if not inventory.has_item(ingredient, quantity):
                return False
        
        # Check requirements
        if 'level' in self.requirements:
            if player.level < self.requirements['level']:
                return False
        
        if 'tool' in self.requirements:
            if not inventory.has_item(self.requirements['tool']):
                return False
        
        return True

class CraftingQueue:
    """Queue for crafting items"""
    
    def __init__(self):
        self.queue = []
    
    def add_to_queue(self, recipe):
        """Add recipe to crafting queue"""
        self.queue.append({
            'recipe': recipe,
            'progress': 0,
            'total_time': recipe.time,
        })
    
    def update(self, dt):
        """Update crafting progress"""
        if self.queue:
            self.queue[0]['progress'] += dt
    
    def get_current_craft(self):
        """Get current crafting item"""
        if self.queue:
            current = self.queue[0]
            progress = current['progress'] / current['total_time']
            return current['recipe'].name, progress
        return None, 0
    
    def complete_craft(self, inventory):
        """Complete current craft and add to inventory"""
        if not self.queue:
            return False
        
        current = self.queue[0]
        if current['progress'] >= current['total_time']:
            recipe = current['recipe']
            inventory.add_item(recipe.output, recipe.quantity)
            self.queue.pop(0)
            return True
        return False
