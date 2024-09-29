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

class Nanobot:
    def __init__(self, name: str, logic: str, type: Nanotype):
        self.name = name
        self.idle_action = None
        self.event_actions = {}
        self.type = type
        self.defense_rating = 1
        self.functional = True
        if self.type == Nanotype.FIGHTER:
            self.defense_rating += 1
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
                # Extract event and action
                parts = line[3:].split()
                event_name = parts[0] if parts else None
                action = parts[1] if len(parts) > 1 else None
                if event_name and action:
                    self.event_actions[event_name] = action

    def get_current_action(self, event: str = None) -> str:
        """Perform the action based on the current event or idle."""
        if not self.functional:
            return "BROKEN"
        if event in self.event_actions:
            return f"Performing {self.event_actions[event]} due to event '{event}'"
        elif self.idle_action:
            return f"Performing idle action: {self.idle_action}"
        return "IDLE"

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

    print(f"Nanobot '{bot_name}' created!")

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
    
    if not nanobot_to_destroy.functional:
        print("Cannot remove a broken robot!")
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

def animated_loading_bar(duration: float) -> None:
    """Display an animated loading bar for the specified duration."""
    total_length = 20
    for i in range(total_length + 1):
        bar = '#' * i + '-' * (total_length - i)
        sys.stdout.write(f'\r[{bar}] {i * 100 // total_length}%')
        sys.stdout.flush()
        time.sleep(duration / total_length)
    print()  # Move to the next line after loading is complete

def handle_fsck(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Fix a nanobot using gold.

    Usage:
        fsck <bot_name> [--quick] [-y]
    """
    
    quick_mode = kwargs.get('quick', False)
    auto_fix = kwargs.get('y', False)

    # Check if the bot name is provided
    if len(args) == 0:
        print("Please provide the name of the nanobot to fsck. Usage: fsck <bot_name>")
        return
    
    bot_name = args[0]  # Get the bot name from the arguments
    
    # Find the nanobot by name
    nanobot_to_fsck = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot_to_fsck is None:
        print(f"No nanobot found with the name '{bot_name}'. Find its name with `ls`!")
        return

    # Check if the nanobot is functional
    print("Running systems check...")
    if not quick_mode:
        animated_loading_bar(3)  # Show loading bar for 3 seconds

    if nanobot_to_fsck.functional:
        print("Nanobot fully functional!")
        return
    
    print("Nanobot is broken!")
    
    # Auto-fix if -y is passed
    if auto_fix:
        do_fsck = True
    else:
        do_fsck = input(f"Do you want to fix {nanobot_to_fsck.name} for {config.fsck_cost} gold? (yes/no): ").strip().lower() in ['yes', 'y']
    
    if do_fsck:
        if player.gold < config.fsck_cost:
            print("Not enough gold to fix the nanobot!")
            return
        if not quick_mode:
            animated_loading_bar(3)  # Show loading bar for 3 seconds
        nanobot_to_fsck.functional = True
        player.gold -= config.fsck_cost
        print(f"Fixed {nanobot_to_fsck.name}!")
    else:
        print("Aborted fix.")
    
    player.save()  # Save changes to the player's data

def handle_truncate(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Truncate the nanobot's logic to the specified length.

    Usage:
        truncate -s <length> <bot_name>
    """
    length = kwargs.get('s')
    
    if length is None or len(args) == 0:
        print("Please provide the length and nanobot name. Usage: truncate -s <length> <bot_name>")
        return
    
    try: 
        length = int(length)
    except TypeError:
        print("Length was not a valid integer! Usage: truncate -s <length> <bot_name>")

    bot_name = args[0]  # Get the bot name from the arguments

    # Find the nanobot by name
    nanobot_to_truncate = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot_to_truncate is None:
        print(f"No nanobot found with the name '{bot_name}'. Find its name with `ls`!")
        return

    # Truncate the logic string
    original_logic = nanobot_to_truncate.logic
    truncated_logic = original_logic[:length]  # Truncate to specified length
    nanobot_to_truncate.logic = truncated_logic
    nanobot_to_truncate.parse_logic()  # Call the parse_logic method

    print(f"Truncated {bot_name}'s logic to:\n{truncated_logic}")
    player.save()  # Save changes to the player's data

def handle_echo(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Echo text to a nanobot's logic.

    Usage:
        echo "idle mine\\non invasion defend" > <bot_name>  # To overwrite
        echo "\\non invasion defend" >> <bot_name> # To append
    """
    if len(args) < 2:
        print("Please provide the text and nanobot name. Usage: echo <text> > <bot_name>")
        return

    text = args[0]  # The text to echo
    text = text.replace("\\n", "\n")
    operator = args[1]  # Operator should be '>' or '>>'
    bot_name = args[2]  # The bot name

    # Find the nanobot by name
    nanobot_to_echo = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot_to_echo is None:
        print(f"No nanobot found with the name '{bot_name}'. Find its name with `ls`!")
        return

    # Handle echoing text based on the operator
    if operator == '>':
        nanobot_to_echo.logic = text  # Overwrite the logic
        print(f"{bot_name}'s logic has been set set.")
    elif operator == '>>':
        nanobot_to_echo.logic += ' ' + text  # Append to the logic
        print(f"Logic appended to {bot_name}.")
    else:
        print("Invalid operator. Use '>' to overwrite or '>>' to append.")
        return

    nanobot_to_echo.parse_logic()  # Call the parse_logic method
    player.save()  # Save changes to the player's data

def handle_cat(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Display the entire logic of the specified nanobot.

    Usage:
        cat <bot_name>
    """
    if len(args) == 0:
        print("Please provide the name of the nanobot. Usage: cat <bot_name>")
        return

    bot_name = args[0]
    nanobot = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot is None:
        print(f"No nanobot found with the name '{bot_name}'.")
        return

    print(nanobot.logic)

def handle_head(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Display the first few lines of the nanobot's logic.

    Usage:
        head <bot_name>
    """
    if len(args) == 0:
        print("Please provide the name of the nanobot. Usage: head <bot_name>")
        return

    bot_name = args[0]
    nanobot = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot is None:
        print(f"No nanobot found with the name '{bot_name}'.")
        return

    # Display the first 3 lines of the logic
    logic_lines = nanobot.logic.splitlines()
    for line in logic_lines[:3]:
        print(line)

def handle_tail(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Display the last few lines of the nanobot's logic.

    Usage:
        tail <bot_name>
    """
    if len(args) == 0:
        print("Please provide the name of the nanobot. Usage: tail <bot_name>")
        return

    bot_name = args[0]
    nanobot = next((bot for bot in player.nanos if bot.name == bot_name), None)

    if nanobot is None:
        print(f"No nanobot found with the name '{bot_name}'.")
        return

    # Display the last 3 lines of the logic
    logic_lines = nanobot.logic.splitlines()
    for line in logic_lines[-3:]:
        print(line)