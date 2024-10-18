# idlegame

[![PyPI](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/pypi.yml)
[![Unit Tests](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml/badge.svg)](https://github.com/bboonstra/idlegame/actions/workflows/tests.yml)

#### PyPI Unit Tests

Ever find yourself stuck at your desk during slow moments in software development? idlegame is here to save the day! Whether you're waiting for a build to finish or just need a quick breather, this idle game is your perfect companion to make those downtime moments more fun and productive. Script your nanobots, collect resources, and defend your filetree, all while learning some handy zsh commands along the way.
## Installation

Getting started with idlegame is a breeze. Open your terminal and run:

```bash
pip install idlegame
```

## Usage

Once it's installed, you can jump right into the game by typing:
```bash
idlegame
```

## Features

+ Easy to Play: Just install and run in 2 simple steps.

+ Casual Gameplay: Perfect for short breaks or when you need to step away from coding.

+ Offline Progress: Your nanobots continue working even when you're not playing.

+ IncrediSave: Automatic saving ensures you'll never lose your progress.

+ zsh Commands: All game commands are valid zsh commands, helping you learn or sharpen your command-line skills.

## How To Play

idlegame is an idle simulation where you script nanobots to collect resources, defend your filetree, and perform other tasks.

### Quickstart

When you first start the game, you’ll be logged in as a user (e.g., bb) and can check on the status of your nanobots by typing:

## How To Play

idlegame is an idle simulation where you script nanobots to collect resources, defend your filetree, and perform other tasks.

### Quickstart

When you first start the game, you’ll be logged in as a user (e.g., bb) and can check on the status of your nanobots by typing:

```bash
bb@idlegame % uptime
```

This will show you how long your nanobots have been working since your last session. Next, you'll need to create a nanobot using a nano core (a key resource in the game). Here's how you can get started:

```bash
bb@idlegame % nano --name mine&defend -y
```
After writing a simple script for your nanobot, it will start working. Here's an example bot script:

```bash
idle mine
on invasion defend
done
```

This bot will mine resources during idle time but switch to defense mode if your filetree is invaded.

## Player's Guide

### Objectives
1. Resource Management: Script nanobots to mine, gather resources, and expand your capabilities.
2. Filetree Defense: Your filetree can be invaded, so it's important to have nanobots ready to defend.
3. Automation Mastery: Efficiently script your nanobots to handle multiple tasks autonomously.
### Commands
+ nano: Create and script nanobots using a nano core.
+ uptime: Check the overall activity and status of your nanobots.
+ man: Get a detailed list of available commands and their usage.

### Strategy Tips
+ Balance Offense and Defense: Create specialized nanobots—some focused on resource mining and others on defending your filetree. Diversify to ensure survival during invasions.
+ Optimize Idle Time: Ensure your nanobots are always doing something useful, whether it's mining, defending, or exploring.
+ Use man Command: When you're stuck, use man to explore all available commands. It’s your go-to guide for learning the ropes.
+ Expand Your Workforce: As you gather more nano cores, create additional nanobots to speed up resource collection and improve defense strategies.
## I'm Stuck!
If you're ever unsure about a command or how to proceed, just type:

```bash
man
```

This will provide a full list of commands or you can run man [command] for specifics on any particular one.

## Contributing
Got ideas or feedback? We’d love to hear from you! Submit a pull request or open an issue on the GitHub repo. Your input helps make idlegame better for everyone.

## License

This project is licensed under the MIT License. Check out the [LICENSE](LICENSE) file for more details.
