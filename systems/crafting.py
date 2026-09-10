"""Inventory and crafting system"""

class Item:
    """Represents an item"""
    
    def __init__(self, item_type, quantity=1):
        self.item_type = item_type
        self.quantity = quantity
    
    def add(self, amount):
        self.quantity += amount
    
    def remove(self, amount):
        if amount >= self.quantity:
            self.quantity = 0
            return amount
        self.quantity -= amount
        return amount

class Inventory:
    """Player inventory"""
    
    def __init__(self, max_slots=30):
        self.items = {}  # {item_type: Item}
        self.max_slots = max_slots
    
    def add_item(self, item_type, quantity=1):
        """Add item to inventory"""
        if len(self.items) < self.max_slots or item_type in self.items:
            if item_type not in self.items:
                self.items[item_type] = Item(item_type, 0)
            self.items[item_type].add(quantity)
            return True
        return False
    
    def remove_item(self, item_type, quantity=1):
        """Remove item from inventory"""
        if item_type in self.items:
            removed = self.items[item_type].remove(quantity)
            if self.items[item_type].quantity <= 0:
                del self.items[item_type]
            return removed
        return 0
    
    def has_item(self, item_type, quantity=1):
        """Check if inventory has item"""
        return item_type in self.items and self.items[item_type].quantity >= quantity
    
    def get_quantity(self, item_type):
        """Get quantity of item"""
        return self.items[item_type].quantity if item_type in self.items else 0
    
    def get_items_list(self):
        """Get list of all items"""
        return list(self.items.keys())

class CraftingSystem:
    """Handles crafting"""
    
    def __init__(self, recipes):
        self.recipes = recipes
        self.crafting_queue = []
    
    def can_craft(self, recipe_name, inventory):
        """Check if recipe can be crafted"""
        if recipe_name not in self.recipes:
            return False
        
        recipe = self.recipes[recipe_name]
        for ingredient, quantity in recipe['ingredients'].items():
            if not inventory.has_item(ingredient, quantity):
                return False
        return True
    
    def craft(self, recipe_name, inventory):
        """Craft an item"""
        if not self.can_craft(recipe_name, inventory):
            return False
        
        recipe = self.recipes[recipe_name]
        
        # Remove ingredients
        for ingredient, quantity in recipe['ingredients'].items():
            inventory.remove_item(ingredient, int(quantity))
        
        # Add output
        inventory.add_item(recipe['output'], recipe['quantity'])
        return True
    
    def get_available_recipes(self, inventory):
        """Get all recipes that can be crafted"""
        available = []
        for recipe_name in self.recipes:
            if self.can_craft(recipe_name, inventory):
                available.append(recipe_name)
        return available
