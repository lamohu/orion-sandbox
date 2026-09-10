"""NPC and dialogue system"""

class NPC:
    """Non-player character"""
    
    def __init__(self, npc_id, name, x, y, dialogue_tree):
        self.npc_id = npc_id
        self.name = name
        self.x = x
        self.y = y
        self.dialogue_tree = dialogue_tree
        self.current_dialogue = 0
        self.faction = 'neutral'
        self.reputation = 0
    
    def get_dialogue(self):
        """Get current dialogue"""
        if self.current_dialogue < len(self.dialogue_tree):
            return self.dialogue_tree[self.current_dialogue]
        return "..."
    
    def next_dialogue(self):
        """Move to next dialogue"""
        self.current_dialogue += 1
    
    def reset_dialogue(self):
        """Reset dialogue to start"""
        self.current_dialogue = 0
    
    def change_reputation(self, amount):
        """Change NPC reputation"""
        self.reputation += amount
    
    def draw(self, surface, camera_offset):
        """Draw NPC"""
        import pygame
        screen_x = int(self.x - camera_offset.x)
        screen_y = int(self.y - camera_offset.y)
        
        # Draw NPC
        pygame.draw.circle(surface, (200, 100, 255), (screen_x, screen_y), 12)
        
        # Draw name above NPC
        font = pygame.font.Font(None, 16)
        name_text = font.render(self.name, True, (255, 255, 255))
        surface.blit(name_text, (screen_x - name_text.get_width() // 2, screen_y - 20))

class DialogueTree:
    """Branching dialogue system"""
    
    def __init__(self):
        self.dialogues = {}
    
    def add_dialogue(self, dialogue_id, text, choices=None):
        """Add dialogue node"""
        self.dialogues[dialogue_id] = {
            'text': text,
            'choices': choices or [],
        }
    
    def get_dialogue(self, dialogue_id):
        """Get dialogue by ID"""
        return self.dialogues.get(dialogue_id, {})

class NPCManager:
    """Manages NPCs in the world"""
    
    def __init__(self):
        self.npcs = {}
        self.dialogue_range = 100
    
    def add_npc(self, npc_id, npc):
        """Add NPC to world"""
        self.npcs[npc_id] = npc
    
    def get_nearby_npc(self, player_pos, range_dist=None):
        """Get NPC within range of player"""
        if range_dist is None:
            range_dist = self.dialogue_range
        
        for npc in self.npcs.values():
            distance = ((player_pos.x - npc.x) ** 2 + (player_pos.y - npc.y) ** 2) ** 0.5
            if distance < range_dist:
                return npc
        return None
    
    def interact_with_npc(self, npc_id):
        """Interact with an NPC"""
        if npc_id in self.npcs:
            npc = self.npcs[npc_id]
            dialogue = npc.get_dialogue()
            npc.next_dialogue()
            return dialogue
        return ""
    
    def draw(self, surface, camera_offset):
        """Draw all NPCs"""
        for npc in self.npcs.values():
            npc.draw(surface, camera_offset)
