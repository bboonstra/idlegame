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
        if not any(bot.name == required_bot for bot in player.nanos):
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

def handle_trivia(player, *args, **kwargs):
    """Lean about zsh, bash, and sh. Get a bonus once per day!"""
    if not is_package_installed(player, 'trivia'):
        print("trivia has not been installed!")
        return

    print("Coming soon...")

def handle_yum(player, *args, **kwargs):
    """Buy things from the shop."""
    if not is_package_installed(player, 'yum'):
        print("yum has not been installed!")
        return

    print("Coming soon...")

def handle_tt(player, *args, **kwargs):
    """TIME TRAVEL!!!1"""
    if not is_package_installed(player, 'timetravel'):
        print("timetravel has not been installed!")
        return

    print("Coming soon...")