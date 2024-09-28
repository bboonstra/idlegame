import difflib
import cmd
import shlex
from idlegame.data import handle_login
from idlegame.idle import handle_claim
from idlegame.profile import handle_profile
import colorama as c
c.init()
class CommandLineInterface(cmd.Cmd):
    prompt = f"{c.Fore.BLUE}idlegame{c.Style.RESET_ALL} {c.Style.DIM}%{c.Style.RESET_ALL} "

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.commands = {
            "logout": self.handle_exit,
            "man": self.handle_man,
            "uptime": handle_claim,
            "idlegame": self.handle_info,
            "alias": self.handle_alias,
            "whoami": handle_profile,
        }

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

    def handle_info(self, player, *args, **kwargs):
        """Learn about idlegame"""
        print("idlegame is a Python package designed to both teach you zsh commands and entertain you while you're bored!\n"
              "Get started: open the manual with `man`")

    def handle_man(self, player, *args, **kwargs):
        """Show help for commands."""
        if args and args[0]:
            command = args[0]
            if command in self.commands:  # Use the commands dictionary to check
                print(self.commands[command].__doc__)
            else:
                print(f" No manual entry for {command}")
        else:
            print("Available commands:")
            for cmd_name in self.commands:
                print(f"  {cmd_name} - {self.commands[cmd_name].__doc__.strip()}")

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
                print(f"Alias '{args[0]}' is not a valid command.")
                return

        if command in self.commands:
            positional, kwargs = self.parse_args(args)
            self.commands[command](self.player, *positional, **kwargs)  # Pass arguments
        else:
            similar_commands = difflib.get_close_matches(command, self.commands.keys())
            if similar_commands:
                print(f"Invalid command. Did you mean: {', '.join(similar_commands)}?")
            else:
                print("Invalid command. Try 'man commands'!")

def main():
    player = handle_login()
    cli = CommandLineInterface(player)
    cli.cmdloop()

if __name__ == '__main__':
    main()
