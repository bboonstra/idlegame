import difflib
import cmd
import shlex
from idlegame.data import handle_login, handle_reboot
from idlegame.idle import handle_claim
from idlegame.profile import handle_profile
from idlegame.nanobots import handle_nano, handle_list, handle_remove, handle_fsck, handle_echo, handle_truncate
from idlegame.nanobots import handle_cat, handle_head, handle_tail
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
        }

    def handle_top(self, player, *args, **kwargs):
        """See your system's complexity and safety level.

        Usage:
            top
        
        This command shows the player's current system complexity and 
        calculates their "safety" level based on the likelihood of high-power invasions.
        """
        # Define safety: scale from 100 (safe) to 0 (dangerous)
        max_complexity = 1000  # This is an arbitrary max limit where it becomes extremely dangerous
        if player.system_complexity < 3:
            safety = 100
        else:
            safety = max(0, round(100 - (player.system_complexity / max_complexity) * 100))
        
        # Print complexity summary
        print(f"System complexity: {player.system_complexity}")
        print("Nanobot contributions to complexity:")
        for bot in player.nanos:
            print(f" - {bot.name}: {bot.complexity} complexity")
        print(f"Aliases contribution: {len(player.aliases) / 10:.1f} complexity")

        # Print safety level
        print(f"Safety level: {safety}% safe")


    def handle_info(self, player, *args, **kwargs):
        """Use this command to learn about idlegame"""
        print("idlegame is a Python package designed to both teach you zsh commands and entertain you while you're bored!\n"
              "Get started: open the manual with `man`")

    def handle_alias(self, player, *args, **kwargs):
        """Set or show your aliases.

        Usage:
            alias <alias_name> <command>
        
        """
        if not args:
            if player.aliases.items():
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
            if command in self.commands and command not in ['sudo']:  # Use the commands dictionary to check
                print(self.commands[command].__doc__)
            else:
                print(f"No manual entry for {command}")
        else:
            print("Available commands:")
            for cmd_name in self.commands:
                if cmd_name not in ['sudo']:
                    if cmd_name in player.packages or cmd_name not in packages.package_requirements.keys():
                        print(f"  {c.Style.BRIGHT}{c.Fore.YELLOW}{cmd_name}{c.Style.RESET_ALL} - {self.commands[cmd_name].__doc__.strip()}\n")

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
                    # Check if the next argument is another flag or if it's a value
                    next_arg = next(iterator)
                    if next_arg.startswith('--'):
                        kwargs[key] = True  # No value, treat as a boolean flag
                        positional.append(next_arg)  # Push the next arg back to iterator
                    else:
                        kwargs[key] = next_arg  # Set value
                except StopIteration:
                    kwargs[key] = True  # No value provided, treat as boolean flag
                    return positional, kwargs
            elif arg.startswith('-'):
                key = arg[1:]  # Remove '-'
                if len(key) == 1:  # Single character flag
                    try:
                        value = next(iterator)  # Get the next argument as value
                        if value.startswith('-'):  # If the next argument is a flag, treat as boolean
                            kwargs[key] = True
                            positional.append(value)  # Push it back to iterator
                        else:
                            kwargs[key] = value  # Set value
                    except StopIteration:
                        kwargs[key] = True  # No value provided, treat as boolean flag
                else:
                    # Handle short options like -abc
                    for char in key:
                        kwargs[char] = True  # Set each character as a flag
                        # You could also handle values here if desired.

            else:
                positional.append(arg)  # Regular positional argument

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
            self.commands[command](self.player, *positional, **kwargs)  # Pass arguments
        else:
            similar_commands = difflib.get_close_matches(command, self.commands.keys())
            if similar_commands:
                print(f"Invalid command. Did you mean {' or '.join(similar_commands)}?")
            else:
                print("Invalid command. Try 'man commands'!")

def main():
    player = handle_login()
    handle_claim(player, automatic=True)
    cli = CommandLineInterface(player)
    cli.prompt = f"{c.Fore.BLUE}{player.username}@idlegame{c.Style.RESET_ALL} {c.Style.DIM}%{c.Style.RESET_ALL} "
    cli.cmdloop()

if __name__ == '__main__':
    main()
