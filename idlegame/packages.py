import random
import subprocess
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init
import re
from idlegame import config
import time
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
                
                # Handle the reward
                reward = item_data['reward']
                if reward.endswith('nanocore'):
                    core_type = reward.split()[0].lower()
                    player.nano_cores[core_type] += 1
                    print(f"You received 1 {core_type} nanocore!")
                elif reward == 'time_crystal':
                    player.time_crystals += 1
                    print("You received 1 Time Crystal!")
                else:
                    print(f"You received: {reward}")

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

    if player.time_crystals < 1:
        print("You need at least one Time Crystal to time travel!")
        return

    print("Preparing for time travel...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Initiating time travel!")

    # Consume a Time Crystal
    player.time_crystals -= 1

    # Generate random time travel effects
    effects = [
        ("Your nanobots have evolved!", lambda: increase_nanobot_efficiency(player)),
        ("You've discovered ancient gold!", lambda: add_gold(player, random.randint(1000, 5000))),
        ("The timeline has shifted, resetting your uptime!", lambda: reset_uptime(player)),
        ("You've glimpsed future technology!", lambda: unlock_random_package(player)),
        ("The fabric of time is damaged, reducing your system complexity!", lambda: reduce_system_complexity(player))
    ]

    # Apply 2-3 random effects
    num_effects = random.randint(2, 3)
    chosen_effects = random.sample(effects, num_effects)

    for effect_message, effect_function in chosen_effects:
        print(effect_message)
        effect_function()

    player.save()
    print("Time travel complete!")

def increase_nanobot_efficiency(player):
    for bot in player.nanobots:
        bot.defense_rating *= 1.2
    print("All nanobots' defense ratings have been increased by 20%!")

def add_gold(player, amount):
    player.gold += amount
    print(f"Added {amount} gold to your account!")

def reset_uptime(player):
    player.last_claim_timestamp = datetime.now(timezone.utc)
    print("Your uptime has been reset to now!")

def unlock_random_package(player):
    available_packages = [pkg for pkg in package_requirements.keys() if pkg not in player.packages]
    if available_packages:
        new_package = random.choice(available_packages)
        player.packages.append(new_package)
        print(f"Unlocked the {new_package} package!")
    else:
        print("No new packages to unlock. Have some gold instead!")
        add_gold(player, 1000)

def reduce_system_complexity(player):    
    reduction = random.randint(5, 10)  # Flat reduction between 5 and 10
    player.complexity_warp += reduction
    player.update_complexity()  # Ensure the complexity is updated
    print(f"Your system complexity has been reduced by {reduction}!")
    print(f"Total complexity warped: {player.complexity_warped}")