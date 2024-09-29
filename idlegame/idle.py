from datetime import datetime, timezone
from data import AutosavedPlayer

def handle_claim(player: AutosavedPlayer) -> None:
    """Claim gold based on the last claim timestamp."""
    now = datetime.now(timezone.utc)  # Use UTC time
    
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
        print("You haven't been offline for long enough to get any rewards!")
        return
    
    player.gold += gold_gain
    
    # Update last claim timestamp to now
    player.last_claim_timestamp = now
    
    print(f"You have claimed {gold_gain} gold for being offline for {minutes_offline} minutes!")
