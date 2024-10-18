idlegame


Ever find yourself stuck at your desk during slow moments in software development? idlegame is here to save the day! Whether you’re waiting for a build to finish or just need a quick breather, this idle game is your perfect companion to make those downtime moments a little more fun.

Installation
Getting started with idlegame is a breeze. Just whip out your terminal and run:

bash
Copy code
pip install idlegame
Usage
Once it’s installed, you can jump right in by typing:

bash
Copy code
idlegame
Features
Easy to Play: Install and run in just two steps!
Casual Gameplay: Ideal for short breaks or when you need to step away from coding.
Offline Play: Your nanobots keep working even when you’re not actively playing.
IncrediSave: Automatic saves mean you’ll never lose progress—it's like magic!
Learn zsh Commands: Every command in idlegame is a valid zsh command, making it a fun way to improve your command-line skills.
How To Play
idlegame serves two purposes: to entertain you at work and to teach you zsh commands. Play the game by scripting nanobots with nano. These nanobots can collect resources, defend your file tree, and more.

Quickstart
zsh
Copy code
Logged in as: bb
bb@idlegame % uptime
Here, you'll see what has happened since you last checked on the uptime of your nanobots.
You can create a nanobot with `nano`, but it requires a nanocore. Here's one to get you started.
Received: 1 basic nano core
bb@idlegame % nano --name mine&defend -y
Write the logic for your nanobot (type 'done' on a new line to finish):
idle mine
on invasion defend
done
Nanobot 'mine&defend' created!
bb@idlegame % ls
Name           Type      Idle Action    Event Actions                 Current Action                
---------------------------------------------------------------------------------------------------- 
mine&defend    Normal    Mine           On invasion: defend           Performing idle action: mine  
---------------------------------------------------------------------------------------------------- 
bb@idlegame % 
This zsh example shows an efficient way to get started. Claim a nano core, and use it to create a nanobot that mines for gold. If someone invades you, the nanobot will help defend.

Player's Guide and Strategy
Getting Started
Create Nanobots: Use your initial nanocores to create versatile nanobots. Experiment with different commands to find what works best for your strategy.
Resource Management: Monitor your resources regularly. Ensure your nanobots are set to collect valuable resources when idle.
Defense Strategy: Set up event actions for your nanobots to defend your file tree. This will help protect your resources from invasions.
Advanced Tips
Optimize Actions: Create specialized nanobots for different tasks (e.g., mining, defense). The more efficient your bots, the better your resource collection.
Explore Commands: Use man to explore all available commands. Familiarizing yourself with the command list will help you strategize better.
Regular Check-Ins: Occasionally check your nanobots’ status to ensure they are functioning as intended.
I'm Stuck
zsh
Copy code
man
Use man to learn about available commands or man [command name] for specifics.

Contributing
Got ideas or feedback? We’d love to hear from you! Feel free to submit a pull request or open an issue on the GitHub repo. Your thoughts can make idlegame even better :>

License
This project is licensed under the MIT License. Check out the LICENSE file for more details.