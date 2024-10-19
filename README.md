# idlegame

[![PyPI](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml)
[![Unit Tests](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml)

Ever find yourself stuck at your desk during slow moments in software development? **idlegame** is here to save the day! Whether you’re waiting for a build to finish or just need a quick breather, this idle game is your perfect companion to make those downtime moments a little more fun.

## Installation

Getting started with **idlegame** is a breeze. Just whip out your terminal and run:

```bash
pip install idlegame
```

## Usage

Once it’s installed, you can jump right in by typing:

```bash
idlegame
```

## Features

- **Easy to Play**: I literally can't think of a way to make it easier. Install and run in 2 steps!
- **Casual Gameplay**: Ideal for short breaks or when you need to step away from coding.
- **Offline Play**: Even when you’re not actively playing, your nanobots are hard at work.
- **IncrediSave**: Automatic saves mean you’ll never lose progress. It’s like magic.
- **Terminal-Based Gameplay**: Emulates a zsh command line for an authentic CLI experience.
- **Nanobot Management**: Create and manage nanobots with various specializations.
- **Resource Gathering**: Mine gold, collect nano cores, and manage your economy.
- **Defense System**: Protect your file tree from invasions.
- **Offline Progression**: Your nanobots work even when you're not actively playing.
- **Educational**: Learn real zsh commands while playing.
- **Upgrades and Packages**: Expand your capabilities as you progress.

## How To Play

**idlegame** is a game made for two purposes. One, to entertain you at work. Two, to teach you some zsh commands.
To that end, every command in idlegame is a valid zsh command (or helper command, or real cli).
Play the game by scripting nanobots with nano. These nanobots can collect resources, defend your filetree, and more.


## Player's Guide

### 1. Create a nanobot
- **Getting Started**
- Use uptime to claim your first nano core.
- Create a nanobot with nano --name miner1 and give it the command idle mine.
- Use ls to view your nanobots and their status.
- Periodically use uptime to claim resources gathered by your nanobots.

- **Key Commands**
- man: Access the manual for game commands.
- nano: Create new nanobots.
- ls: List your nanobots and their actions.
- uptime: Claim offline progress and rewards.
- rm: Remove a nanobot (and reclaim its core).
- whoami: Check your profile and stats.
- apt: Install new packages (once unlocked).

- **Nanobot Types**
- Normal: Versatile, basic nanobots.
- Miner: Specialized in gold mining.
- Fighter: Enhanced defense capabilities.
- Super: Excels in both mining and defense.
- Warper: Unique time-manipulation abilities.
- Researcher: Improves learning and upgrades.
- Hacker: Specialized in finding vulnerabilities.
- Diplomat: Enhances connections and trade.

- **Strategy Tips**
- Balanced Approach: Create a mix of miner and defender nanobots early on.
- Upgrade Regularly: Use apt to install new packages and expand your capabilities.
- Manage Complexity: Keep an eye on your system complexity with top. Higher complexity attracts stronger invasions.
- Use Aliases: Create aliases for frequently used commands to save time.
- Defend Wisely: Ensure you have enough defending nanobots before logging off for extended periods.
- Explore Commands: Experiment with different commands to discover hidden features and strategies.

- **Advanced Features**
- Time Travel: Use time crystals for powerful temporal effects.
- Research Points: Accumulate and spend on advanced upgrades.
- Connections: Establish diplomatic connections for trade benefits.
- Hacking: Attempt to gain resources through system vulnerabilities.

- **idlegame** is a game that evolves with your skills and knowledge of zsh commands

### Quickstart

```zsh
Logged in as: bb
bb@idlegame % uptime
Here, you'll be able to see what has happened since you last checked on the uptime of your nanobots.
You can create a nanobot with `nano`, but it requires a nanocore. Here's one to get you started.
Recieved: 1 basic nano core
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
```

The zsh above shows an efficient way to get started. Claim a nano core, and use it to create a Nanobot that mines for gold. However, if someone invades you, the Nanobot will help defend. This is a very useful all-purpose bot.

## I'm stuck

```zsh
man
```

`man` will tell you anything you need to know! It will list all the commands available to you, or use `man [command name]` to get specifics.

## Contributing

Got ideas or feedback? We’d love to hear from you! Feel free to submit a pull request or open an issue on the GitHub repo. Your thoughts can make **idlegame** even better :>

## License

This project is licensed under the MIT License. Check out the [LICENSE](LICENSE) file for more details.
