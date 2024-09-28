from datetime import datetime, timezone
from data import AutosavedPlayer

def handle_claim(player: AutosavedPlayer, *args, **kwargs) -> None:
    """Claim rewards in the game.

    Usage:
        claim [--reward <reward>] [--silent]
    
    Options:
        --reward <reward>  Specify the reward to claim.
        --silent           Suppress output messages.
    """
    now = datetime.now(timezone.utc)  # Use UTC time
    
    # Check for the --silent option
    silent_mode = kwargs.get('silent', False)

    if player.last_claim_timestamp is None:
        # If the player has never claimed, just set it to now
        player.last_claim_timestamp = now
        player.save()
        print("You have claimed your first reward of 100 gold!")
        player.gold += 100
        return

    # Calculate time difference since last claim
    time_offline = now - player.last_claim_timestamp
    minutes_offline = int(time_offline.total_seconds() // 60)
    gold_gain = minutes_offline
    if minutes_offline < 1:
        if not silent_mode:
            print("You haven't been offline for long enough to get any rewards!")
        return
    
    player.gold += gold_gain
    
    # Update last claim timestamp to now
    player.last_claim_timestamp = now
    
    if not silent_mode:
        print(f"You have claimed {gold_gain} gold for being offline for {minutes_offline} minutes!")
