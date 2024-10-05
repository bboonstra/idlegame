import random
import subprocess
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init
import re
from idlegame import config
init()

# Define package requirements
package_requirements = {
    'apt': {},
    'yum': {
        'gold': 500,
        'nano_cores': 1,
    },
    'trivia': {
        'gold': 100,
    },
    'timetravel': {
        'gold': 1000000,
        'warper_cores': 1,
        'required_names': ['Emmett Brown']
    },
}

def install_package(player, package_name):
    """Install a package for the player if they meet the requirements."""
    if is_package_installed(player, package_name):
        return
    
    requirements = package_requirements.get(package_name, 'Invalid')

    if requirements == 'Invalid':
        print(f"{package_name} is not a valid package.")
        return

    # Check if player meets the requirements
    if player.gold < requirements.get('gold', 0):
        print(f"You need {requirements.get('gold', 0)} gold to install {package_name}.")
        return

    if player.nano_cores['normal'] < requirements.get('nano_cores', 0):
        print(f"You need {requirements.get('nano_cores', 0)} nanocores to install {package_name}.")
        return
    
    if player.nano_cores['warper'] < requirements.get('warper_cores', 0):
        print(f"You need {requirements.get('warper_cores', 0)} warper nanocores to install {package_name}.")
        return

    for required_bot in requirements.get('required_bots', []):
        if not any(bot.name == required_bot for bot in player.nanobots):
            print(f"You need a nanobot named '{required_bot}' to install {package_name}.")
            return

    # Deduct costs and install the package
    player.gold -= requirements.get('gold', 0)
    player.nano_cores['normal'] -= requirements.get('nano_cores', 0)
    player.nano_cores['warper'] -= requirements.get('warper_cores', 0)

    player.packages.append(package_name)
    player.save()
    print(f">> {package_name} has been installed! You can try it out with `{package_name}`.")

def is_package_installed(player, package_name):
    """Check if a package is already installed for the player."""
    return package_name in player.packages

def show_available_packages(player):
    """Display packages available for installation."""
    print("Available packages to install:")
    for package in package_requirements.keys():
        if is_package_installed(player, package):
            continue
        requirements = package_requirements.get(package)
        if requirements:
            requirement_msg_parts = []

            # Collect requirement messages dynamically
            if requirements.get('gold', 0) > 0:
                requirement_msg_parts.append(f"Gold: {requirements['gold']}")
            if requirements.get('nano_cores', 0) > 0:
                requirement_msg_parts.append(f"Nanocores: {requirements['nano_cores']}")
            if requirements.get('warper_cores', 0) > 0:
                requirement_msg_parts.append(f"Warper nanocores: {requirements['warper_cores']}")
            if requirements.get('required_names'):
                required_bots = ', '.join(requirements['required_names'])
                requirement_msg_parts.append(f"Requires you to have a nanobot with the name: {required_bots}")

            requirement_msg = ', '.join(requirement_msg_parts) if requirement_msg_parts else 'No requirements'
            print(f"{package} | {requirement_msg}")

def handle_apt(player, *args, **kwargs):
    """Get and install packages."""
    if not is_package_installed(player, 'apt'):
        print("apt has not been installed!")
        return

    show_available_packages(player)

    selection = input("Enter the name of a package to try to install, or press Enter to quit: ")
    if selection in package_requirements.keys():
        install_package(player, selection)
    elif selection:
        print(f"{selection} is not a valid package.")


def get_random_zsh_command():
    """Pull a random Zsh command from the system."""
    try:
        # Get a list of available commands using compgen in Zsh
        result = subprocess.run(["zsh", "-ic", "compgen -c"], capture_output=True, text=True)
        commands = result.stdout.splitlines()
        if commands:
            # Randomly select a command from the list
            return random.choice(list(filter(lambda cmd: not cmd.startswith('_'), commands)))
        else:
            print("No commands found.")
            return None
    except subprocess.CalledProcessError:
        print("Error fetching Zsh commands.")
        return None

def get_command_description(command):
    """Get a description of a command using 'whatis' or 'man'."""
    try:
        # Use 'whatis' to get a brief description of the command
        result = subprocess.run(["whatis", command], capture_output=True, text=True)
        description = result.stdout.strip()

        if description:
            description = description.splitlines()[0].split('-')[1].strip()
            # Replace the command name with question marks equal to the command's length
            question_marks = "[???]"
            # Replace variations of the command name (add more variations as needed)
            variations = [command, command.lower(), command.upper()]
            for variation in variations:
                # \b denotes a word boundary, ensuring we match whole words only
                description = re.sub(r'\b' + re.escape(variation) + r'\b', question_marks, description)

            if len(description) > 50:
                return description[:50] + "..."
            return description
        else:
            return f"No description available for {command}."
    except subprocess.CalledProcessError:
        return f"Error fetching description for {command}."


def handle_trivia(player, *args, **kwargs):
    """Learn about zsh, bash, and sh. Get a bonus once per day!"""

    # Cooldown settings
    cooldown_period = timedelta(minutes=10)
    current_time = datetime.now(timezone.utc)

    # Check if the cooldown has passed
    if player.last_trivia_timestamp is not None:
        last_attempt_time = player.last_trivia_timestamp
        if current_time < last_attempt_time + cooldown_period:
            remaining_time = (last_attempt_time + cooldown_period) - current_time
            print(f"Your next trivia will be available in {remaining_time.seconds // 60} minutes and {remaining_time.seconds % 60} seconds!")
            return

    attempts = 5  # Limit the number of rerolls to prevent an infinite loop
    command = None
    description = None
    
    print("Loading trivia from your system...")
    # Reroll the command if the description says "No description available"
    for _ in range(attempts):
        # Get a random Zsh command
        command = get_random_zsh_command()
        if not command:
            print("Could not fetch a random command.")
            return
        
        # Get the description for the random command
        description = get_command_description(command)
        
        # Check if description is valid
        if "No description available" not in description:
            break
        else:
            print(f"Rerolling... No description available for {command}.")
    else:
        print("Failed to find a valid command in your ZSH system with a description.")
        return

    print(f"What is the name of this command?\n{Fore.GREEN}>> {description} <<{Style.RESET_ALL}")

    # Ask the player for the command
    user_input = input("% ").strip()

    # Check if the user's answer is correct
    if user_input == command:
        print("That's correct!")
        gold_award = max(round(player.gold * (random.random() / 10)), 100)
        player.gold += gold_award
        print(f"You have been awarded {gold_award} gold!")
        
        # Check for daily bonus
        if player.last_trivia_bonus_timestamp is None or current_time >= player.last_trivia_bonus_timestamp + timedelta(days=1):
            bonus_gold = gold_award * 10  # 10x bonus
            player.gold += bonus_gold
            player.last_trivia_bonus_timestamp = current_time
            print(f"Daily bonus awarded! You receive an additional {bonus_gold} gold!")
        else:
            print("You have already claimed your daily bonus.")
    else:
        print(f"Nope! The correct answer was: {command}")

    player.last_trivia_timestamp = current_time

def reroll_shop(player):
    player.shop_data = {}
    player.shop_timestamp = datetime.now(timezone.utc)
    available_items = list(config.shop_items.items())
    selected_items = random.sample(available_items, min(3, len(available_items)))
    for item_name, item_data in selected_items:
        player.shop_data[item_name] = item_data

def handle_yum(player, *args, **kwargs):
    """Buy things from the shop."""
    if not is_package_installed(player, 'yum'):
        print("yum has not been installed!")
        return
    if not player.shop_data or (datetime.now(timezone.utc) - player.shop_timestamp).total_seconds() / 3600 >= config.shop_cooldown_hours:
        # set up the shop
        reroll_shop(player)

    print("Available items:")
    for item_name, item_data in player.shop_data.items():
        print(f"{item_name}: {item_data['description']} - {item_data['price_gold']} gold")

    while True:
        item_to_buy = input("Enter the name of the item you want to buy (or 'cancel' to exit): ").strip().lower()
        
        if item_to_buy == 'cancel':
            print("Purchase cancelled.")
            return

        # Create a dictionary with lowercase keys for comparison
        lowercase_shop_keys = {k.strip().lower(): k for k in player.shop_data.keys()}

        if item_to_buy in lowercase_shop_keys:
            original_key = lowercase_shop_keys[item_to_buy]
            item_data = player.shop_data[original_key]
            if player.gold >= item_data['price_gold']:
                player.gold -= item_data['price_gold']
                print(f"You bought {original_key} for {item_data['price_gold']} gold!")
                # Here you would add logic to give the player the item they bought
                del player.shop_data[original_key]  # Remove the item from the shop after purchase
                player.save()  # Save the player's updated state
                break
            else:
                print(f"You don't have enough gold to buy this item. You need {item_data['price_gold']} gold.")
        else:
            print("Invalid item name. Please try again.")

def handle_tt(player, *args, **kwargs):
    """TIME TRAVEL!!!1"""
    if not is_package_installed(player, 'timetravel'):
        print("timetravel has not been installed!")
        return

    print("Coming soon...")