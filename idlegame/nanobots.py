from enum import Enum
from typing import List

class Nanotype(Enum):
    NORMAL = 1
    SPECIAL = 2

class Nanobot:
    def __init__(self, name: str, logic: str, type: Nanotype):
        self.name = name
        self.logic = logic
        self.type = type

class Player:
    def __init__(self):
        self.nanobots: List[Nanobot] = []
        self.nano_cores = {'normal': 1, 'special': 1}  # Example initial resources

    def save(self):
        print("Player data saved.")

class AutosavedPlayer(Player):
    def save(self):
        super().save()

def handle_nano(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Write a new nanobot with interactive multi-line editing support.

        Usage:
            nano [--type <nanotype>] [--name <name>] [-y]
        
        Requires:
            1 Nano Core
            --type: 1 typed core

        Scripting:
            Use the interactive editor to input the nanobot's logic.
            Use commands to navigate and modify lines:
            - insert <line number> <text>: Insert text at a specific line number
            - delete <line number>: Delete a specific line
            - edit <line number> <new text>: Edit a specific line
            - show: Show the current logic being edited
            - done: Finish editing and save the nanobot
        """
    
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
    if any(bot.name == bot_name for bot in player.nanobots):
        print("Error: A bot with this name already exists. Please choose a unique name.")
        return

    print("Starting interactive logic editor for your nanobot.")
    
    # In-memory editor logic
    logic_lines = []
    
    while True:
        command = input("Enter command (insert, delete, edit, show, done): ").strip().lower()
        if command == "done":
            break
        elif command.startswith("insert"):
            _, line_num_str, *line_text = command.split()
            line_num = int(line_num_str)
            line_text = " ".join(line_text)
            logic_lines.insert(line_num, line_text)
        elif command.startswith("delete"):
            _, line_num_str = command.split()
            line_num = int(line_num_str)
            if 0 <= line_num < len(logic_lines):
                logic_lines.pop(line_num)
            else:
                print("Invalid line number.")
        elif command.startswith("edit"):
            _, line_num_str, *new_text = command.split()
            line_num = int(line_num_str)
            new_text = " ".join(new_text)
            if 0 <= line_num < len(logic_lines):
                logic_lines[line_num] = new_text
            else:
                print("Invalid line number.")
        elif command == "show":
            print("Current logic:")
            for i, line in enumerate(logic_lines):
                print(f"{i}: {line}")
        else:
            print("Invalid command. Available commands: insert, delete, edit, show, done.")

    # Finalize logic
    nano_logic = '\n'.join(logic_lines)
    
    new_nanobot = Nanobot(name=bot_name, logic=nano_logic.strip(), type=nanobot_type)
    player.nanobots.append(new_nanobot)
    player.nano_cores['normal'] -= 1
    if bot_type:
        player.nano_cores[bot_type.lower()] -= 1
    player.save()

    print(f"Nanobot '{bot_name}' created with the following logic:\n{nano_logic}")

# Example of how to use this function
player = AutosavedPlayer()
handle_nano(player, type='normal', name='BotAlpha', y=True)
