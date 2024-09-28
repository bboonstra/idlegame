from .data import AutosavedPlayer

def handle_profile(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Check your profile.

    Usage:
        whoami [--short]
    
    Options:
        --short           Cut down on the size.
    """
         
    short = kwargs.get('short', False)

    if short:
        print(f"Level: {player.level} ({player.experience} exp) | HP: {player.hp}\nGold: {player.gold}")
    else:
        print(f"--- {player.username} ---\n"
              f"- Level: {player.level} ({player.experience} exp)\n"
              f"- HP: {player.hp}\n"
              f"- Gold: {player.gold}")
