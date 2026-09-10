"""Advanced input handling"""
import pygame

class InputHandler:
    """Handles all user input"""
    
    def __init__(self):
        self.keys_pressed = {}
        self.mouse_buttons = {}
        self.mouse_pos = (0, 0)
        self.key_bindings = {
            'move_up': pygame.K_w,
            'move_down': pygame.K_s,
            'move_left': pygame.K_a,
            'move_right': pygame.K_d,
            'attack': pygame.K_SPACE,
            'inventory': pygame.K_e,
            'crafting': pygame.K_c,
            'building': pygame.K_b,
            'mining': pygame.K_m,
            'pause': pygame.K_ESCAPE,
        }
    
    def update(self):
        """Update input state"""
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = {
            'left': pygame.mouse.get_pressed()[0],
            'middle': pygame.mouse.get_pressed()[1],
            'right': pygame.mouse.get_pressed()[2],
        }
    
    def is_key_pressed(self, action):
        """Check if action key is pressed"""
        if action in self.key_bindings:
            key_code = self.key_bindings[action]
            return self.keys_pressed[key_code]
        return False
    
    def is_mouse_button_pressed(self, button):
        """Check if mouse button is pressed"""
        return self.mouse_buttons.get(button, False)
    
    def get_movement_vector(self):
        """Get movement input as vector"""
        x = 0
        y = 0
        
        if self.is_key_pressed('move_up'):
            y -= 1
        if self.is_key_pressed('move_down'):
            y += 1
        if self.is_key_pressed('move_left'):
            x -= 1
        if self.is_key_pressed('move_right'):
            x += 1
        
        return (x, y)
    
    def rebind_key(self, action, key_code):
        """Change key binding"""
        if action in self.key_bindings:
            self.key_bindings[action] = key_code
