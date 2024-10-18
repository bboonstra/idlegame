idlegame
PyPI Unit Tests
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
Easy to Play: I literally can't think of a way to make it easier. Install and run in 2 steps!
Casual Gameplay: Ideal for short breaks or when you need to step away from coding.
Offline Play: Even when you’re not actively playing, your nanobots are hard at work.
IncrediSave: Automatic saves mean you’ll never lose progress. It’s like magic.
Educational: Learn zsh commands while playing!
How To Play
idlegame is a game made for two purposes: to entertain you at work and to teach you some zsh commands. Every command in idlegame is a valid zsh command (or helper command, or real CLI). Play the game by scripting nanobots with nano. These nanobots can collect resources, defend your file tree, and more.

Quickstart
Logged in as: bb
bash
Copy code
bb@idlegame % uptime
Here, you'll be able to see what has happened since you last checked on the uptime of your nanobots.

You can create a nanobot with nano, but it requires a nanocore. Here's one to get you started.

bash
Copy code
Recieved: 1 basic nano core
bb@idlegame % nano --name mine&defend -y
Write the logic for your nanobot (type 'done' on a new line to finish):
idle mine
on invasion defend
done
Nanobot 'mine&defend' created!

bash
Copy code
bb@idlegame % ls
Name           Type      Idle Action    Event Actions                 Current Action                
----------------------------------------------------------------------------------------------------
mine&defend    Normal    Mine           On invasion: defend           Performing idle action: mine  
----------------------------------------------------------------------------------------------------
The zsh above shows an efficient way to get started. Claim a nanocore and use it to create a Nanobot that mines for gold. However, if someone invades you, the Nanobot will help defend. This is a very useful all-purpose bot.

Strategies for Success
Diversify Your Nanobots: Create different types of nanobots for various tasks (mining, defense, etc.).
Monitor Uptime: Regularly check the uptime to assess the performance and efficiency of your nanobots.
Utilize Commands: Make full use of the man command to learn more about the game commands and their functionalities.
Upgrade Regularly: As you gain resources, consider upgrading your nanobots to enhance their capabilities.
I'm Stuck
bash
Copy code
man
man will tell you anything you need to know! It will list all the commands available to you, or use man [command name] to get specifics.

Contributing
Got ideas or feedback? We’d love to hear from you! Feel free to submit a pull request or open an issue on the GitHub repo. Your thoughts can make idlegame even better :>

License
This project is licensed under the MIT License. Check out the LICENSE file for more details.
