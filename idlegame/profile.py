from idlegame.data import AutosavedPlayer

def handle_profile(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Check your profile.

    Usage:
        whoami [--short]
    
    Options:
        --short           Cut down on the size.
    """
         
    short = kwargs.get('short', False)

    if short:
        print(f"System Complexity: {player.system_complexity} | Tree Health: {player.tree_health}\n"
              f"Gold: {player.gold} | Nanobots: {len(player.nanos)}")
    else:
        print(f"--- {player.username} ---\n"
              f"- System Complexity: {player.system_complexity} (see top)\n"
              f"- Tree Health: {player.tree_health}\n"
              f"- Gold: {player.gold}\n"
              f"- Nanobots: {len(player.nanos)} (see ls)")
