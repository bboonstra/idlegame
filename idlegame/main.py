import difflib
from data import handle_login, AutosavedPlayer
from idle import handle_claim

def main():
    def command_exit(player: AutosavedPlayer, *args):
        print("Cya later!")
        quit()
    
    def command_help(player: AutosavedPlayer, *args):
        print("Available commands:")
        for command in commands.keys():
            print(f"- {command}")

    def command_claim(player: AutosavedPlayer, *args):
        handle_claim(player)

    # Map commands to functions, including aliases
    commands = {
        "exit": command_exit,
        "quit": command_exit,
        "help": command_help,
        "claim": command_claim,
        "c": command_claim,
    }

    # Main game loop
    player: AutosavedPlayer = handle_login()
    while True:
        inp = input("What would you like to do? ")
        
        # Split input into command and arguments
        parts = inp.split()
        command = parts[0]
        args = parts[1:]

        # Check for command and execute
        if command in commands:
            commands[command](player, *args)  # Pass arguments if needed
        else:
            # Suggest similar commands
            similar_commands = difflib.get_close_matches(command, commands.keys())
            if similar_commands:
                print(f"Invalid command. Did you mean: {', '.join(similar_commands)}?")
            else:
                print("Invalid command. Try 'help'!")

if __name__ == '__main__':
    main()
