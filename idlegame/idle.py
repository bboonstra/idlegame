from datetime import datetime, timezone, timedelta
from idlegame.data import AutosavedPlayer
from idlegame.battle import simulate_defense
import idlegame.config as config
from idlegame.packages import install_package
import random

def handle_claim(player: AutosavedPlayer, *args, **kwargs) -> None:
    """See what occurred while you were offline!

    Usage:
        uptime [--silent]
    
    Options:
        --silent           Suppress output messages.
    """

    now = datetime.now(timezone.utc)  # Use UTC time
    
    # Check for the --silent option
    silent_mode = kwargs.get('silent', False)
    automatic = kwargs.get('automatic', False)

    if player.last_claim_timestamp is None:
        if automatic:
            return
        # If the player has never claimed, initialize last claim timestamp and give 1 core.
        player.last_claim_timestamp = now
        player.nano_cores['normal'] += 1
        player.save()
        print("Here, you'll be able to see what has happened since you last checked on the uptime of your nanobots.")
        print("You can create a nanobot with `nano`, but it requires a nanocore. Here's one to get you started.")
        print("Recieved: 1 basic nano core")
        return

    # Calculate time difference since last claim
    time_offline = now - player.last_claim_timestamp
    total_seconds_offline = int(time_offline.total_seconds())
    
    if total_seconds_offline < 600:
        if (not automatic) and (not silent_mode):
            print("Nothing has happened yet. You need to wait for at least 10 minutes to claim rewards!")
        return
    
    num_chunks = total_seconds_offline // config.sim_chunk_duration

    gold_gathered = 0
    invasions_total = 0
    nanobots_broken = 0

    # Simulate each 10-minute chunk
    for _ in range(num_chunks):
        invasion_occurred = random.random() < config.invasion_chance_per_chunk

        # Collect all defenders for this chunk
        defending_bots = []

        for bot in player.nanos:
            # Bot does nothing if broken
            if not bot.functional:
                continue

            # Do event actions if applicable
            for event, action in bot.event_actions.items():
                if event.lower() in ['battle.defense', 'defense', 'invasion'] and action in ['defend', 'join', 'support', 'defense'] and invasion_occurred:
                    defending_bots.append(bot)
                    continue
            else:
                # Otherwise do idle actions
                if bot.idle_action in ['mine', 'mining', 'miner']:
                    gold_gathered += config.base_mining_rate  # mine resources for this chunk
                if bot.idle_action in ['defend', 'defense', 'defending']:
                    defending_bots.append(bot)

        # Simulate defense if an invasion occurred
        if invasion_occurred:
            invasions_total += 1
            nanobots_broken += simulate_defense(player, defending_bots)
            # TODO logic if you lose

    
    # Add gathered gold to player
    player.gold += gold_gathered

    # Update last claim timestamp to reflect only complete chunked increments
    leftover_time = total_seconds_offline % config.sim_chunk_duration
    player.last_claim_timestamp = now - timedelta(seconds=leftover_time)
    player.save()

    # Print the results unless in silent mode
    if not silent_mode:
        print(f"You were offline for {total_seconds_offline // 60} minutes.")
        print(f"You mined {gold_gathered} gold!")
        print(f"{invasions_total} invasions occurred during your offline time.")
        if nanobots_broken > 0:
            print(f"{nanobots_broken} of your bots was broken during the invasions.")
    
    install_package(player, 'apt')
