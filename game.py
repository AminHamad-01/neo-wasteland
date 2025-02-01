import random
import time
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum, auto
import asyncio
from datetime import datetime

class GameState(Enum):
    MAIN_MENU = auto()
    EXPLORING = auto()
    COMBAT = auto()
    INVENTORY = auto()
    SHOP = auto()
    CRAFTING = auto()
    QUEST_LOG = auto()
    DYING = auto()

@dataclass
class Stats:
    strength: int
    agility: int
    intelligence: int
    tech_aptitude: int

    def calculate_bonus(self, stat_value: int) -> int:
        return (stat_value - 10) // 2

class StatusEffect:
    def __init__(self, name: str, duration: int, effect_dict: Dict[str, int]):
        self.name = name
        self.duration = duration
        self.effects = effect_dict
        self.start_time = datetime.utcnow()

class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    CONSUMABLE = auto()
    QUEST = auto()
    CYBERNETIC = auto()

@dataclass
class Item:
    name: str
    type: ItemType
    rarity: int  # 1-5
    level_req: int
    effects: Dict[str, int]
    description: str
    value: int
    durability: Optional[int] = None

class CombatStyle(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    TECHNICAL = "technical"

class Character:
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.stats = Stats(10, 10, 10, 10)
        self.health = 100
        self.max_health = 100
        self.energy = 100
        self.max_energy = 100
        self.experience = 0
        self.credits = 100
        self.inventory: List[Item] = []
        self.equipped: Dict[str, Item] = {}
        self.status_effects: List[StatusEffect] = []
        self.combat_style = CombatStyle.AGGRESSIVE
        self.cybernetics: List[Item] = []
        self.reputation: Dict[str, int] = {
            "Netrunners": 0,
            "Corporates": 0,
            "Wasteland": 0
        }
        
    @property
    def damage_bonus(self) -> int:
        return self.stats.calculate_bonus(self.stats.strength)

    @property
    def defense_bonus(self) -> int:
        return self.stats.calculate_bonus(self.stats.agility)

    def apply_status_effect(self, effect: StatusEffect):
        self.status_effects.append(effect)

    def update_status_effects(self):
        current_time = datetime.utcnow()
        self.status_effects = [
            effect for effect in self.status_effects
            if (current_time - effect.start_time).seconds < effect.duration
        ]

class QuestState(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class QuestObjective:
    description: str
    target_amount: int = 1
    current_amount: int = 0
    completed: bool = False

class Quest:
    def __init__(self, name: str, description: str, level_req: int):
        self.name = name
        self.description = description
        self.level_req = level_req
        self.objectives: List[QuestObjective] = []
        self.rewards: Dict[str, int] = {}
        self.state = QuestState.NOT_STARTED
        self.deadline: Optional[datetime] = None

class Location:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.connected_locations: List['Location'] = []
        self.npcs: List['NPC'] = []
        self.items: List[Item] = []
        self.danger_level: int = 1
        self.requires_keycard: bool = False

class GameEngine:
    def __init__(self):
        self.player = None
        self.current_state = GameState.MAIN_MENU
        self.locations: List[Location] = []
        self.current_location: Optional[Location] = None
        self.quests: List[Quest] = []
        self.game_time = datetime.utcnow()
        self.save_dir = "saves"
        self.last_save = None
        self.load_game_data()

    def load_game_data(self):
        """Load game data from JSON files"""
        try:
            with open('data/items.json', 'r') as f:
                self.item_templates = json.load(f)
            with open('data/locations.json', 'r') as f:
                self.location_templates = json.load(f)
            with open('data/quests.json', 'r') as f:
                self.quest_templates = json.load(f)
        except FileNotFoundError:
            print("Warning: Game data files not found. Creating new templates...")
            self.create_default_templates()

    def create_default_templates(self):
        """Create default game data if no files exist"""
        os.makedirs('data', exist_ok=True)
        
        # Create default items
        default_items = {
            "weapons": [
                {
                    "name": "Quantum Blade",
                    "type": "WEAPON",
                    "rarity": 4,
                    "level_req": 5,
                    "effects": {"damage": 45, "energy_cost": 15},
                    "description": "A blade that exists in multiple dimensions",
                    "value": 500
                }
            ],
            # Add more default items...
        }
        
        with open('data/items.json', 'w') as f:
            json.dump(default_items, f, indent=4)

    async def game_loop(self):
        while True:
            self.update_game_state()
            await self.handle_input()
            await asyncio.sleep(0.1)  # Prevent CPU hogging

    def update_game_state(self):
        if self.player:
            self.player.update_status_effects()
            self.update_quests()
            self.update_world()

    def update_quests(self):
        for quest in self.quests:
            if quest.state == QuestState.IN_PROGRESS:
                if quest.deadline and datetime.utcnow() > quest.deadline:
                    quest.state = QuestState.FAILED

    def update_world(self):
        """Update world state, NPCs, and dynamic events"""
        self.game_time = datetime.utcnow()
        # Update NPC positions
        # Update dynamic events
        # Update weather/environment

    def save_game(self):
        """Save game state to file"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        save_data = {
            "player": self.player.__dict__,
            "current_location": self.current_location.name if self.current_location else None,
            "quests": self.quests,
            "game_time": self.game_time.isoformat()
        }
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.save_dir, f"save_{timestamp}.json")
        
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=4)
        
        self.last_save = save_path
        print(f"Game saved to {save_path}")

class CombatEngine:
    def __init__(self, player: Character, enemy: Character):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.combat_log: List[str] = []

    async def execute_combat_round(self):
        """Execute a single round of combat"""
        # Initiative based on agility
        participants = sorted(
            [self.player, self.enemy],
            key=lambda x: x.stats.agility,
            reverse=True
        )

        for attacker in participants:
            if attacker.health <= 0:
                continue

            defender = self.enemy if attacker == self.player else self.player
            await self.process_attack(attacker, defender)

    async def process_attack(self, attacker: Character, defender: Character):
        """Process attack logic with combat styles and status effects"""
        base_damage = attacker.damage_bonus
        
        # Apply combat style modifiers
        if attacker.combat_style == CombatStyle.AGGRESSIVE:
            base_damage *= 1.2
        elif attacker.combat_style == CombatStyle.DEFENSIVE:
            defender.defense_bonus *= 1.2
        elif attacker.combat_style == CombatStyle.TECHNICAL:
            # Technical attacks have a chance to apply status effects
            if random.random() < 0.3:
                effect = StatusEffect("Stunned", 2, {"agility": -2})
                defender.apply_status_effect(effect)

        # Calculate final damage
        damage = max(0, base_damage - defender.defense_bonus)
        defender.health -= damage
        
        self.combat_log.append(
            f"{attacker.name} deals {damage} damage to {defender.name}"
        )

class UserInterface:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.current_menu = []
        self.menu_stack = []

    def push_menu(self, menu_items: List[str]):
        """Push a new menu onto the stack"""
        self.menu_stack.append(self.current_menu)
        self.current_menu = menu_items
        self.display_current_menu()

    def pop_menu(self):
        """Return to the previous menu"""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            self.display_current_menu()

    def display_current_menu(self):
        """Display the current menu with formatting"""
        print("\n" + "="* 50)
        print(f"Location: {self.engine.current_location.name if self.engine.current_location else 'Main Menu'}")
        print(f"Credits: {self.engine.player.credits if self.engine.player else 0}")
        print("=" * 50)
        
        for i, item in enumerate(self.current_menu, 1):
            print(f"{i}. {item}")

def main():
    engine = GameEngine()
    ui = UserInterface(engine)
    
    try:
        asyncio.run(engine.game_loop())
    except KeyboardInterrupt:
        print("\nSaving game...")
        engine.save_game()
        print("Game saved. Goodbye!")

if __name__ == "__main__":
    main()