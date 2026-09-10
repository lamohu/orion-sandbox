"""UI rendering system"""
import pygame

class UIPanel:
    """Base UI panel"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
    
    def draw(self, surface):
        """Draw panel background"""
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height), 2)
    
    def on_mouse_click(self, x, y):
        """Handle mouse click"""
        return (self.x <= x < self.x + self.width and 
                self.y <= y < self.y + self.height)

class HUD:
    """Heads-up display showing player stats"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
    
    def draw(self, surface, player):
        """Draw HUD elements"""
        # Health display
        health_text = self.font_small.render(f"Health: {int(player.health)}/{int(player.max_health)}", True, (0, 255, 0))
        surface.blit(health_text, (10, 10))
        
        # Hunger display
        hunger_text = self.font_small.render(f"Hunger: {int(player.hunger)}/{int(player.max_hunger)}", True, (255, 200, 0))
        surface.blit(hunger_text, (10, 40))
        
        # Level display
        level_text = self.font_small.render(f"Level: {player.level}", True, (100, 200, 255))
        surface.blit(level_text, (10, 70))
        
        # Experience display
        exp_to_level = player.level * 100
        exp_text = self.font_small.render(f"XP: {int(player.experience)}/{exp_to_level}", True, (200, 100, 255))
        surface.blit(exp_text, (10, 100))
        
        # Inventory count
        inv_count = len(player.inventory.items)
        inv_text = self.font_small.render(f"Inventory: {inv_count}/{player.inventory.max_slots}", True, (255, 255, 255))
        surface.blit(inv_text, (10, 130))

class InventoryUI(UIPanel):
    """Inventory display"""
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, 20)
        self.selected_item = None
    
    def draw(self, surface, player):
        """Draw inventory"""
        if not self.visible:
            return
        
        super().draw(surface)
        
        # Draw title
        title = self.font.render("Inventory", True, (255, 255, 255))
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Draw items
        y_offset = self.y + 40
        for item_type, item in player.inventory.items.items():
            item_text = self.font.render(f"{item_type}: {item.quantity}", True, (200, 200, 200))
            surface.blit(item_text, (self.x + 20, y_offset))
            y_offset += 25

class CraftingUI(UIPanel):
    """Crafting menu"""
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, 18)
        self.selected_recipe = None
        self.recipes = []
    
    def draw(self, surface, available_recipes):
        """Draw crafting menu"""
        if not self.visible:
            return
        
        super().draw(surface)
        
        # Draw title
        title = self.font.render("Crafting", True, (255, 255, 255))
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Draw recipes
        y_offset = self.y + 40
        for i, recipe in enumerate(available_recipes):
            color = (255, 200, 0) if recipe == self.selected_recipe else (200, 200, 200)
            recipe_text = self.font.render(recipe, True, color)
            surface.blit(recipe_text, (self.x + 20, y_offset))
            y_offset += 22
    
    def select_recipe(self, index, available_recipes):
        """Select a recipe"""
        if 0 <= index < len(available_recipes):
            self.selected_recipe = available_recipes[index]

class BuildingUI(UIPanel):
    """Building menu"""
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, 18)
        self.building_types = ['wall', 'door', 'chest', 'campfire', 'tower']
        self.selected_building = None
    
    def draw(self, surface):
        """Draw building menu"""
        if not self.visible:
            return
        
        super().draw(surface)
        
        # Draw title
        title = self.font.render("Buildings", True, (255, 255, 255))
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Draw building types
        y_offset = self.y + 40
        for i, building in enumerate(self.building_types):
            color = (255, 200, 0) if building == self.selected_building else (200, 200, 200)
            building_text = self.font.render(building, True, color)
            surface.blit(building_text, (self.x + 20, y_offset))
            y_offset += 22
    
    def select_building(self, index):
        """Select a building type"""
        if 0 <= index < len(self.building_types):
            self.selected_building = self.building_types[index]
            return self.selected_building
        return None

class PauseMenu(UIPanel):
    """Pause menu"""
    
    def __init__(self, width, height):
        menu_width = 300
        menu_height = 200
        super().__init__(width // 2 - menu_width // 2, height // 2 - menu_height // 2, menu_width, menu_height)
        self.font = pygame.font.Font(None, 32)
        self.options = ['Resume', 'Settings', 'Exit']
        self.selected = 0
    
    def draw(self, surface):
        """Draw pause menu"""
        if not self.visible:
            return
        
        # Darken background
        dark_surface = pygame.Surface((surface.get_width(), surface.get_height()))
        dark_surface.set_alpha(128)
        dark_surface.fill((0, 0, 0))
        surface.blit(dark_surface, (0, 0))
        
        # Draw menu
        super().draw(surface)
        
        # Draw title
        title = self.font.render("PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 30))
        surface.blit(title, title_rect)
        
        # Draw options
        y_offset = self.y + 80
        for i, option in enumerate(self.options):
            color = (255, 200, 0) if i == self.selected else (200, 200, 200)
            option_text = self.font.render(option, True, color)
            surface.blit(option_text, (self.x + 50, y_offset))
            y_offset += 40
