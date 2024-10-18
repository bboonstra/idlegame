import difflib
import cmd
import shlex
from idlegame.data import handle_login, handle_reboot
from idlegame.idle import handle_claim, handle_crontab
from idlegame.profile import handle_profile
from idlegame.nanobots import (
    handle_nano, handle_list, handle_remove, 
    handle_fsck, handle_echo, handle_truncate, 
    handle_cat, handle_head, handle_tail
)
from idlegame.config import handle_sudo
import idlegame.packages as packages
import colorama as c

c.init()

class CommandLineInterface(cmd.Cmd):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.commands = {
            "logout": self.handle_exit,
            "bye": self.handle_exit,
            "exit": self.handle_exit,
            "man": self.handle_man,
            "uptime": handle_claim,
            "idlegame": self.handle_info,
            "alias": self.handle_alias,
            "whoami": handle_profile,
            "crontab": handle_crontab,
            "nano": handle_nano,
            "rm": handle_remove,
            "ls": handle_list,
            "sudo": handle_sudo,
            "fsck": handle_fsck,
            "echo": handle_echo,
            "truncate": handle_truncate,
            "cat": handle_cat,
            "head": handle_head,
            "tail": handle_tail,
            "top": self.handle_top,
            "apt": packages.handle_apt,
            "yum": packages.handle_yum,
            "trivia": packages.handle_trivia,
            "timetravel": packages.handle_tt,
            "reboot": handle_reboot,
            "ssh": self.handle_ssh,
            "nmap": self.handle_nmap,
            "research": self.handle_research,
        }

    def handle_top(self, player, *args, **kwargs):
        """See your system's complexity and safety level."""
        max_complexity = 1000
        if player.system_complexity < 3:
            safety = 100
        else:
            safety = max(0, round(100 - (player.system_complexity / max_complexity) * 100))

        print(f"System complexity: {player.system_complexity}")
        print("Nanobot contributions to complexity:")
        for bot in player.nanobots:
            print(f" - {bot.name}: {bot.complexity} complexity")
        print(f"Aliases contribution: {len(player.aliases) / 10:.1f} complexity")
        print(f"Safety level: {safety}% safe")

    def handle_info(self, player, *args, **kwargs):
        """Use this command to learn about idlegame."""
        print("idlegame is a Python package designed to both teach you zsh commands and entertain you while you're bored!\n"
              "Get started: open the manual with `man`")

    def handle_alias(self, player, *args, **kwargs):
        """Set or show your aliases."""
        if not args:
            if player.aliases:
                print("Current aliases:")
                for alias, command in player.aliases.items():
                    print(f"  {alias} -> {command}")
            else:
                print("No aliases set. Set one with alias <alias_name> <command>")
            return

        alias = args[0]
        command = ' '.join(args[1:])
        if alias in self.commands.keys():
            print("You can't set an alias name to a command. Maybe you switched around the alias order?")
            return

        if command:
            player.aliases[alias] = command
            player.save()
            print(f"Alias set: {alias} -> {command}")
        else:
            print("Usage: alias <alias_name> <command>")

    def handle_man(self, player, *args, **kwargs):
        """Show help for commands."""
        if args and args[0]:
            command = args[0]
            if command in self.commands and command not in ['sudo']:
                print(self.commands[command].__doc__)
            else:
                print(f"No manual entry for {command}")
        else:
            print("Available commands:")
            for cmd_name in self.commands:
                if cmd_name not in ['sudo']:
                    if cmd_name in player.packages or cmd_name not in packages.package_requirements.keys():
                        print(f"  {c.Style.BRIGHT}{c.Fore.YELLOW}{cmd_name}{c.Style.RESET_ALL} - {self.commands[cmd_name].__doc__.strip()}")

    def handle_nmap(self, player, *args, **kwargs):
        """Scan for vulnerabilities."""
        print(f"Total scan attempts: {player.scan_attempts}")
        print(f"Successful scans: {player.scan_successes}")
        if player.scan_attempts > 0:
            print(f"Success rate: {player.scan_successes / player.scan_attempts:.2%}")
        else:
            print("Make a nanobot `hack` when idle to scan for vulnerabilities!")

    def handle_ssh(self, player, *args, **kwargs):
        """Manage connections with other systems."""
        if not player.connections:
            print("You have no active connections.")
            print("Make a nanobot `connect` when idle to scan for vulnerabilities!")
            print("Diplomatic connections are made by `connect`ing with idle nanobots. Connections help you defend against invasions and gain gold through trade.")
        else:
            print("Your active connections:")
            for connection in player.connections:
                print(f"- {connection}")

    def handle_research(self, player, *args, **kwargs):
        """View research points and available upgrades."""
        print(f"You have {player.research_points} research points.")
        # TODO: Implement research upgrades

    def handle_exit(self, player, *args, **kwargs):
        """Exit the game."""
        print("Cya later!")
        quit()

    def parse_args(self, args):
        """Parses positional and keyword arguments from the input."""
        kwargs = {}
        positional = []
        iterator = iter(args)

        for arg in iterator:
            if arg.startswith('--'):
                key = arg[2:]  # Remove '--'
                try:
                    next_arg = next(iterator)
                    if next_arg.startswith('--'):
                        kwargs[key] = True
                        positional.append(next_arg)
                    else:
                        kwargs[key] = next_arg
                except StopIteration:
                    kwargs[key] = True
                    return positional, kwargs
            elif arg.startswith('-'):
                key = arg[1:]  # Remove '-'
                if len(key) == 1:
                    try:
                        value = next(iterator)
                        if value.startswith('-'):
                            kwargs[key] = True
                            positional.append(value)
                        else:
                            kwargs[key] = value
                    except StopIteration:
                        kwargs[key] = True
                else:
                    for char in key:
                        kwargs[char] = True

            else:
                positional.append(arg)

        return positional, kwargs

    def do_help(self, player, *args, **kwargs):
        """Override the default help command."""
        print("Use 'man <command>' for help.")

    def default(self, line):
        # Split input and handle quoted strings
        args = shlex.split(line)
        command = args[0]
        args = args[1:]

        # Check for aliases
        if command in self.player.aliases.keys():
            command = self.player.aliases[command]
            if command not in self.commands:
                print(f"Your alias is set to '{command}', but that is not a valid command.")
                return

        if command in self.commands:
            positional, kwargs = self.parse_args(args)
            self.commands[command](self.player, *positional, **kwargs)
        else:
            similar_commands = difflib.get_close_matches(command, self.commands.keys())
            if similar_commands:
                print(f"Invalid command. Did you mean {' or '.join(similar_commands)}?")
            else:
                print("Invalid command. Try 'man'!")

def main():
    player = handle_login()
    cli = CommandLineInterface(player)
    cli.prompt = f"{c.Fore.BLUE}{player.username}@idlegame{c.Style.RESET_ALL} {c.Style.DIM}%{c.Style.RESET_ALL} "
    cli.cmdloop()

if __name__ == '__main__':
    main()
