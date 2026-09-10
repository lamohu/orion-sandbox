"""Enhanced UI components and menus"""
import pygame

class Button:
    """Clickable button"""
    
    def __init__(self, x, y, width, height, text, color=(100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 50, 255) for c in color)
        self.is_hovered = False
        self.font = pygame.font.Font(None, 20)
    
    def update(self, mouse_pos):
        """Update button hover state"""
        self.is_hovered = (self.x <= mouse_pos[0] <= self.x + self.width and
                          self.y <= mouse_pos[1] <= self.y + self.height)
    
    def draw(self, surface):
        """Draw button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

class ProgressBar:
    """Visual progress bar"""
    
    def __init__(self, x, y, width, height, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.value = 0
        self.max_value = 100
    
    def set_value(self, value, max_value):
        """Set progress value"""
        self.value = value
        self.max_value = max_value
    
    def draw(self, surface):
        """Draw progress bar"""
        percentage = self.value / self.max_value if self.max_value > 0 else 0
        filled_width = self.width * percentage
        
        pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, (self.x, self.y, filled_width, self.height))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)

class Tooltip:
    """Tooltip for UI elements"""
    
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 16)
        self.surface = self.font.render(text, True, (255, 255, 0))
        self.visible = False
    
    def draw(self, surface):
        """Draw tooltip"""
        if self.visible:
            pygame.draw.rect(surface, (50, 50, 50), 
                           (self.x, self.y, self.surface.get_width() + 10, self.surface.get_height() + 5))
            surface.blit(self.surface, (self.x + 5, self.y + 2))

class QuestLogUI(UIPanel):
    """Quest log display"""
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.font = pygame.font.Font(None, 18)
        self.scroll_offset = 0
    
    def draw(self, surface, quest_system):
        """Draw quest log"""
        if not self.visible:
            return
        
        super().draw(surface)
        
        # Draw title
        title = self.font.render("Active Quests", True, (255, 255, 255))
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Draw quests
        y_offset = self.y + 40
        for quest in quest_system.get_active_quests():
            progress_text = f"{quest.name}: {int(quest.progress)}/{quest.objective}"
            quest_text = self.font.render(progress_text, True, (200, 200, 200))
            surface.blit(quest_text, (self.x + 20, y_offset))
            y_offset += 22

class MainMenu:
    """Main menu screen"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_title = pygame.font.Font(None, 64)
        self.font_button = pygame.font.Font(None, 32)
        
        # Buttons
        button_width = 200
        button_height = 50
        center_x = width // 2 - button_width // 2
        
        self.buttons = {
            'start': Button(center_x, 200, button_width, button_height, 'Start Game'),
            'settings': Button(center_x, 270, button_width, button_height, 'Settings'),
            'quit': Button(center_x, 340, button_width, button_height, 'Quit'),
        }
    
    def update(self, mouse_pos):
        """Update menu"""
        for button in self.buttons.values():
            button.update(mouse_pos)
    
    def draw(self, surface):
        """Draw menu"""
        surface.fill((20, 20, 40))
        
        # Draw title
        title = self.font_title.render('Orion Sandbox', True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        surface.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(surface)
    
    def handle_click(self, mouse_pos):
        """Handle mouse click"""
        for button_name, button in self.buttons.items():
            if button.is_clicked(mouse_pos):
                return button_name
        return None
