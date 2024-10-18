idlegame
Introduction
idlegame is a Python-based simulation game designed to both teach you zsh commands and entertain you in your downtime. It challenges players to build an unstoppable army of nanobots by gathering resources, defending your filetree, and using various commands in a zsh-like environment.

Features:
Command-line Gameplay: Emulates a zsh-like command prompt to play the game.
Nanobots: Create, manage, and upgrade your nanobots to gather resources and defend your system.
Commands:
nano: Create a new nanobot.
rm: Remove nanobots and reclaim their resources.
ls: List nanobots and their current logic.
fsck: Fix and upgrade nanobots using gold.
echo: Modify nanobot logic by echoing commands.
top: View system complexity and safety levels.
reboot: Reset the game and delete all save data.
Player’s Guide
Getting Started
To begin, simply run the game using:

bash
Copy code
python run.py
You’ll be greeted with a welcome message and can begin by typing one of the available commands. The primary objective is to create and manage nanobots that will work on your behalf to gather resources and protect your file system.

Commands
nano: Create new nanobots to perform tasks. Nanobots need Nano Cores and specific logic for what they should do (e.g., idle mine or on invasion defend).

Example:

bash
Copy code
nano --type core --name miner
ls: Lists all your nanobots and their current jobs.

rm: Remove a nanobot to reclaim resources.

Example:

bash
Copy code
rm miner
fsck: Fix and upgrade nanobots using gold.

echo: Modify a nanobot's logic. This allows you to program nanobots for different tasks.

Example:

bash
Copy code
echo "idle mine\non invasion defend" > miner
top: View your system's complexity and safety level, which depends on the number of nanobots and their tasks.

Strategy Tips
Balance Resource Gathering and Defense:

Use nano to create nanobots that gather resources (idle mine), but don’t forget to have defense bots (on invasion defend) ready in case your system comes under attack.
Upgrade and Fix Nanobots:

Use fsck to upgrade and fix nanobots when they get damaged. This ensures they can keep working at peak efficiency.
Avoid System Overload:

Monitor your system's complexity with top. A high complexity increases the risk of invasions, so balance nanobot creation and defense.
Use Aliases to Save Time:

If you find yourself using certain commands frequently, set up aliases to speed up gameplay.
Don't Forget to Backup:

Before making major changes, you might want to save your progress. The reboot command will reset everything, so be cautious when using it.
Game Objectives
Main Objective: Build a robust nanobot army to gather resources and defend your system from invasions.
Secondary Objectives: Upgrade nanobots, improve your system's safety, and try to maintain balance between complexity and defense.
Credits
© 2024 Ben Boonstra | MIT License