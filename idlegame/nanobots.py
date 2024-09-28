from idlegame.data import AutosavedPlayer
from enum import Enum

class Nanotype(Enum):
    NORMAL = "normal"
    MINER = "miner"
    FIGHTER = "fighter"
    SUPER = "super"
    WARPER = "warper"

class Nanobot:
    def __init__(self, name: str, logic: str, type: Nanotype):
        self.name = name
        self.idle_action = None
        self.event_actions = {}
        self.type = type
        self.defense_rating = 1
        if self.type == Nanotype.FIGHTER:
            self.defense_rating += 1
        self.parse_logic(logic)

    def parse_logic(self, logic: str) -> None:
        """Parse the nanobot logic and set idle and event actions."""
        lines = logic.strip().splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("idle "):
                self.idle_action = line[5:].strip()
            elif line.startswith("on "):
                # Extract event and action
                parts = line[3:].split()
                event_name = parts[0] if parts else None
                action = parts[1] if len(parts) > 1 else None
                if event_name and action:
                    self.event_actions[event_name] = action

    def get_current_action(self, event: str = None) -> str:
        """Perform the action based on the current event or idle."""
        if event in self.event_actions:
            return f"Performing {self.event_actions[event]} due to event '{event}'"
        elif self.idle_action:
            return f"Performing idle action: {self.idle_action}"
        return "IDLE"

    def __repr__(self):
        return f"Nanobot(name={self.name}, idle_action={self.idle_action}, event_actions={self.event_actions})"

def handle_nano(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Write a new nanobot.

        Usage:
            nano [--type <nanotype>] [--name <name>] [-y]
        
        Requires:
            1 Nano Core
            --type: 1 typed core

        Scripting:
            Use the `idle` parameter for an idle job
            Use the `on` parameter for an event-driven job
            Use the `done` parameter to finish scripting
            Example:
                idle mine
                on attacking attack
                on defending defend
                done

        """
    
    bot_type = kwargs.get('type', None)
    bot_name = kwargs.get('name', None)
    auto_accept = kwargs.get('y', False) is not False

    if player.nano_cores.get('normal', 0) < 1:
        print("You need at least 1 nano core to create a new nanobot.")
        return
    
    if bot_type and player.nano_cores.get(bot_type.lower(), 0) < 1:
        print(f"You need at least 1 {bot_type.lower()} core to create a specialized nanobot.")
        return
    
    # Determine the nanobot type
    if bot_type:
        nanobot_type = Nanotype[bot_type.upper()]
    else:
        nanobot_type = Nanotype.NORMAL

    if not auto_accept:
        create_nano = input(f"Do you want to create a new {nanobot_type.name.lower()} nanobot? (yes/no): ").strip().lower()
        if create_nano not in ['yes', 'y']:
            print("No new nanobot created.")
            return

    if not bot_name:
        bot_name = input("Enter a name for your nanobot: ")
    
    if len(bot_name) > 15 or any(bot.name == bot_name for bot in player.nanos):
        print("Invalid name. Names must be unique and less than 16 characters long.")
        return
    
    # Interactive session for nano logic input
    print("Write the logic for your nanobot (type 'done' on a new line to finish):")
    nano_logic_lines = []
    
    while True:
        line = input()
        if line.strip().lower() == 'done':
            break
        nano_logic_lines.append(line)

    # Join the lines into a single string
    nano_logic = '\n'.join(nano_logic_lines)

    # Create a new Nanobot instance and add it to the player's nanos list
    new_nanobot = Nanobot(name=bot_name, logic=nano_logic.strip(), type=nanobot_type)
    player.nanos.append(new_nanobot)
    player.nano_cores['normal'] -= 1  # Deduct a nano core for creating a new nanobot
    if bot_type:
        player.nano_cores[bot_type.lower()] -= 1  # Deduct a specialized core if applicable
    player.save()  # Save changes to the player's data

    print(f"Nanobot '{bot_name}' created with logic:\nIdle action: {new_nanobot.idle_action}\nEvent actions: {new_nanobot.event_actions}.")


def handle_remove(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Remove a nanobot and reclaim its nano core(s).

    Usage:
        rm <bot_name>
    """
    
    # Check if the bot name is provided
    if len(args) == 0:
        print("Please provide the name of the nanobot to remove. Usage: rm <bot_name>")
        return
    
    bot_name = args[0]  # Get the bot name from the arguments
    
    # Find the nanobot by name
    nanobot_to_destroy = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot_to_destroy is None:
        print(f"No nanobot found with the name '{bot_name}'. Find its name with `ls`!")
        return

    # Reclaim the core(s) based on the nanobot type
    player.nano_cores['normal'] += 1  # Reclaiming a normal core
    
    core_type = None
    if nanobot_to_destroy.type != Nanotype.NORMAL:
        core_type = nanobot_to_destroy.type.name.lower()
        player.nano_cores[core_type] += 1  # Reclaiming the typed core if applicable

    # Remove the nanobot from the list
    player.nanos.remove(nanobot_to_destroy)
    player.save()  # Save changes to the player's data

    # Print the appropriate message based on nanobot type
    if nanobot_to_destroy.type != Nanotype.NORMAL:
        print(f"Nanobot '{bot_name}' destroyed. You have reclaimed 1 normal core and 1 {core_type} core.")
    else:
        print(f"Nanobot '{bot_name}' destroyed. You have reclaimed 1 normal core.")

def handle_list(player: AutosavedPlayer, *args, **kwargs) -> None:
    """List all nanobots and their current logic.

    Usage:
        ls
    """
    
    if not player.nanos:
        print("You have no nanobots.")
        return

    # Header
    print(f"{'Name':<15}{'Type':<10}{'Idle Action':<15}{'Event Actions':<30}{'Current Action':<30}")
    print("-" * 100)

    # Loop through each nanobot and display relevant details
    for bot in player.nanos:
        idle_action = bot.idle_action or "None"
        current_action = bot.get_current_action() or "None"
        event_actions = list(bot.event_actions.items())

        # Print the first event action on the same line as the bot's other details
        if event_actions:
            first_event, first_action = event_actions[0]
            first_event_text = f"On {first_event}: {first_action}"
            print(f"{bot.name:<15}{bot.type.name.capitalize():<10}{idle_action.capitalize():<15}{first_event_text:<30}{current_action:<30}")
        else:
            print(f"{bot.name:<15}{bot.type.name.capitalize():<10}{idle_action.capitalize():<15}{'None':<30}{current_action:<30}")
        
        # Print additional event actions (if any) on new lines, aligned with the event actions column
        for event, action in event_actions[1:]:
            text = f"On {event}: {action}"
            print(f"{'':<15}{'':<10}{'':<15}{text:<60}")

    print("-" * 100)
