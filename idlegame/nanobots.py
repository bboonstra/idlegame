import tkinter as tk
from tkinter import filedialog, messagebox
from idlegame.data import AutosavedPlayer
from enum import Enum
from idlegame import config
import time
import sys

class Nanotype(Enum):
    NORMAL = "normal"
    MINER = "miner"
    FIGHTER = "fighter"
    SUPER = "super"
    WARPER = "warper"
    RESEARCHER = "researcher"
    HACKER = "hacker"
    DIPLOMAT = "diplomat"

class Nanobot:
    def __init__(self, name: str, logic: str, type: Nanotype):
        self.name = name
        self.idle_action = None
        self.event_actions = {}
        self.type = type
        self.defense_rating = 1
        self.mining_rate = 1
        self.functional = True
        self.warp_chance = 0
        self.research_rate = 0
        self.scan_success_rate = 0.01
        self.connection_rate = 0.1
        self.learn_rate = 0.2
        
        if self.type == Nanotype.MINER:
            self.mining_rate = 1.3
        elif self.type == Nanotype.FIGHTER:
            self.defense_rating = 1.3
        elif self.type == Nanotype.SUPER:
            self.mining_rate = 1.3
            self.defense_rating = 1.3
        elif self.type == Nanotype.WARPER:
            self.warp_chance = 0.1
        elif self.type == Nanotype.RESEARCHER:
            self.learn_rate = 0.5
        elif self.type == Nanotype.HACKER:
            self.scan_success_rate = 0.2
        elif self.type == Nanotype.DIPLOMAT:
            self.connection_rate = 0.3
        
        self.logic = logic
        self.complexity = 0
        self.update_complexity()
        self.parse_logic()

    def update_complexity(self):
        self.complexity = (len(self.logic) / 10) * (2 if self.type != Nanotype.NORMAL else 1)

    def parse_logic(self) -> None:
        """Parse the nanobot logic and set idle and event actions."""
        lines = self.logic.strip().splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("idle "):
                self.idle_action = line[5:].strip()
            elif line.startswith("on "):
                parts = line[3:].split()
                event_name = parts[0] if parts else None
                action = parts[1] if len(parts) > 1 else None
                if event_name and action:
                    self.event_actions[event_name] = action

    def get_current_action(self, event=None) -> str:
        """Perform the action based on the current event or idle."""
        if not self.functional:
            return "BROKEN"
        if event in self.event_actions:
            return f"Performing {self.event_actions[event]} due to event '{event}'"
        elif self.idle_action:
            return f"Performing idle action: {self.idle_action}"
        return "IDLE"

def handle_nano(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Write a new nanobot."""
    bot_type = kwargs.get('type')
    bot_name = kwargs.get('name')
    auto_accept = kwargs.get('y', False) is not False

    if player.nano_cores.get('normal', 0) < 1:
        print("You need at least 1 nano core to create a new nanobot.")
        return
    
    if bot_type and player.nano_cores.get(bot_type.lower(), 0) < 1:
        print(f"You need at least 1 {bot_type.lower()} core to create a specialized nanobot.")
        return
    
    nanobot_type = Nanotype[bot_type.upper()] if bot_type else Nanotype.NORMAL

    if not auto_accept and input(f"Do you want to create a new {nanobot_type.name.lower()} nanobot? (yes/no): ").strip().lower() not in ['yes', 'y']:
        print("No new nanobot created.")
        return

    if not bot_name:
        bot_name = input("Enter a name for your nanobot: ")
    
    if len(bot_name) > 15:
        print("Error: Bot name is too long. Please choose a name with 15 characters or fewer.")
        return

    print("Write the logic for your nanobot (type 'done' on a new line to finish):")
    nano_logic ⬤
