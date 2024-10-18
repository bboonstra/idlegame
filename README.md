# idlegame

[![PyPI](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml)
[![Unit Tests](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml)

Ever find yourself stuck at your desk during slow moments in software development? **idlegame** is here to save the day! Whether you’re waiting for a build to finish or just need a quick breather, this idle game is your perfect companion to make those downtime moments a little more fun.

idlegame
Overview
idlegame is a game designed for two purposes: to entertain you during work and to teach you essential zsh commands. In this game, every command is a valid zsh command, allowing you to play while learning.

Getting Started
Installation
Clone the repository:
bash
Copy code
git clone <repository-url>
Navigate to the directory:
bash
Copy code
cd idlegame
Install the requirements:
bash
Copy code
pip install -r requirements.txt
Running the Game
To start the game, run:

bash
Copy code
python run.py
Player's Guide
Commands
Creating a Nanobot: Use the nano command to create a nanobot.

bash
Copy code
nano --name <bot_name> [-y]
Example:

bash
Copy code
nano --name mine&defend -y
Listing Nanobots: Use ls to list all nanobots and their statuses.

Removing a Nanobot: Use rm <bot_name> to remove a nanobot and reclaim its nano core.

Fixing a Nanobot: Use fsck <bot_name> to fix a malfunctioning nanobot.

Echoing Logic: Use echo to overwrite or append logic to a nanobot.

bash
Copy code
echo "idle mine\non invasion defend" > <bot_name>  # To overwrite
echo "\non invasion defend" >> <bot_name> # To append
Viewing Nanobot Logic:

Display Full Logic: cat <bot_name>
Display First Few Lines: head <bot_name>
Display Last Few Lines: tail <bot_name>
Truncate Logic: truncate -s <length> <bot_name>
Utility Commands
Logout Commands:

logout - Exit the game.
bye - Exit the game.
exit - Exit the game.
Help Command:

man - Show help for commands.
Uptime Command:

uptime - See what occurred while you were offline!
Usage: uptime [--silent]
Options: --silent - Suppress output messages.
Learn about idlegame:

idlegame - Use this command to learn about idlegame.
Aliases:

alias - Set or show your aliases.
Usage: alias <alias_name> <command>
Profile Check:

whoami - Check your profile.
Usage: whoami [--short]
Options: --short - Cut down on the size.
Cron Commands:

crontab - See what commands are ready to be used.
System Monitoring:

top - See your system's complexity and safety level.
Usage: top
System Management:

reboot - DELETES ALL SAVE DATA.
ssh - Manage connections with other systems.
nmap - Scan for vulnerabilities.
research - View research points and available upgrades.
Features
Interactive Nanobots: Create nanobots that can mine resources, defend your filetree, and respond to events.
Event-Driven Actions: Script your nanobots with event-driven logic to enhance their capabilities.
Resource Management: Manage your nano cores to create specialized nanobots for various tasks.
Strategies
Resource Allocation: Balance the creation of normal and specialized nanobots based on your resource needs.
Event Handling: Utilize event actions effectively to ensure your nanobots respond appropriately to various situations.
Maintenance: Regularly check and fix your nanobots to keep them operational and efficient.
Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss changes.

License
This project is licensed under the MIT License.


