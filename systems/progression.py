"""Quest and progression system"""

class Quest:
    """Represents a quest"""
    
    def __init__(self, quest_id, name, description, objective, reward):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objective = objective
        self.reward = reward
        self.progress = 0
        self.completed = False
    
    def update_progress(self, amount):
        """Update quest progress"""
        self.progress += amount
        if self.progress >= self.objective:
            self.completed = True
            return True
        return False
    
    def claim_reward(self, player):
        """Claim quest reward"""
        if self.completed:
            if 'experience' in self.reward:
                player.gain_experience(self.reward['experience'])
            if 'items' in self.reward:
                for item_type, quantity in self.reward['items'].items():
                    player.inventory.add_item(item_type, quantity)
            return True
        return False

class QuestSystem:
    """Manages quests"""
    
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.initialize_quests()
    
    def initialize_quests(self):
        """Initialize available quests"""
        quests = [
            Quest('gather_wood', 'Gather Wood', 'Collect 10 wood', 10, 
                  {'experience': 50, 'items': {'stone': 5}}),
            Quest('gather_stone', 'Gather Stone', 'Collect 20 stone', 20, 
                  {'experience': 75, 'items': {'iron': 2}}),
            Quest('craft_sword', 'Craft Sword', 'Craft a wooden sword', 1, 
                  {'experience': 100, 'items': {'wood': 10}}),
            Quest('kill_goblins', 'Kill Goblins', 'Defeat 5 goblins', 5, 
                  {'experience': 150, 'items': {'gold': 3}}),
            Quest('kill_boss', 'Defeat Boss', 'Defeat the fire elemental', 1, 
                  {'experience': 500, 'items': {'diamond': 5, 'gold': 10}}),
        ]
        
        for quest in quests:
            self.quests[quest.quest_id] = quest
    
    def add_quest(self, quest_id):
        """Add quest to active quests"""
        if quest_id in self.quests and quest_id not in [q.quest_id for q in self.active_quests]:
            self.active_quests.append(self.quests[quest_id])
            return True
        return False
    
    def complete_quest(self, quest_id, player):
        """Complete a quest"""
        for quest in self.active_quests:
            if quest.quest_id == quest_id:
                quest.claim_reward(player)
                self.active_quests.remove(quest)
                self.completed_quests.append(quest)
                return True
        return False
    
    def get_active_quests(self):
        """Get all active quests"""
        return self.active_quests

class ProgressionSystem:
    """Handles player progression and tech trees"""
    
    def __init__(self):
        self.unlocked_recipes = set()
        self.unlocked_buildings = set()
        self.milestones = {
            'first_tool': False,
            'first_house': False,
            'first_boss': False,
            'max_level': False,
        }
    
    def unlock_recipe(self, recipe_name):
        """Unlock a crafting recipe"""
        self.unlocked_recipes.add(recipe_name)
    
    def unlock_building(self, building_type):
        """Unlock a building type"""
        self.unlocked_buildings.add(building_type)
    
    def check_milestones(self, player):
        """Check if player has achieved milestones"""
        # First tool milestone
        if (not self.milestones['first_tool'] and 
            any(tool in player.inventory.get_items_list() 
                for tool in ['wooden_pickaxe', 'stone_pickaxe', 'iron_pickaxe'])):
            self.milestones['first_tool'] = True
            player.gain_experience(100)
            return 'first_tool'
        
        # Max level milestone
        if not self.milestones['max_level'] and player.level >= 20:
            self.milestones['max_level'] = True
            player.gain_experience(200)
            return 'max_level'
        
        return None
