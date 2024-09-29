from typing import List
from idlegame.data import AutosavedPlayer
from idlegame.nanobots import Nanobot
import random

def simulate_defense(player: AutosavedPlayer, defending_bots: List[Nanobot]) -> int:
    """Simulate defense against invasions using the given nanobots.

    Args:
        player (AutosavedPlayer): The player who owns the nanobots.
        defending_bots (List[Nanobot]): The nanobots assigned to defend.

    Returns:
        int: The number of nanobots that were broken during the defense.
    """
    if not defending_bots:
        return 0  # No bots to defend

    # Calculate total defense power from the defending bots
    total_defense_power = 0
    for bot in defending_bots:
        total_defense_power += bot.defense_rating
        if bot.idle_action in ['defend', 'defense', 'guard', 'defender']:
            total_defense_power += 1

    # Simulate the invasion strength
    invasion_strength = max(round((random.random() + 0.1) * (player.system_complexity - 3)), 0)
    print(f"Invasion strength: {invasion_strength}, Total defense power: {total_defense_power}")

    # Calculate the ratio of defense power to invasion strength
    defense_ratio = total_defense_power / invasion_strength if invasion_strength > 0 else 1

    # Determine the chance of breaking bots based on defense ratio
    # If defense_ratio is high, break chance is low; if low, break chance is high
    # Exponential scaling for break chance:
    if defense_ratio >= 2:
        break_chance = 0  # Strong advantage
    elif defense_ratio >= 1:
        break_chance = (1 - (defense_ratio - 1) / 1) * 0.5  # Linear decrease
    else:
        # Exponential growth in break chance for heavily disadvantaged scenario
        break_chance = min(1, 0.5 * (1 - defense_ratio))  # Break chance up to 50% max

    bots_broken = 0

    # Determine how many bots break based on calculated break chance
    for bot in defending_bots:
        if random.random() < break_chance:
            bot.functional = False
            print(f"One of your defending bots, '{bot.name}', was broken during an invasion! Repair it with `fsck`.")
            bots_broken += 1

    if bots_broken == 0:
        print(f"Your defenses held against an invasion (Strength: {invasion_strength}).")

    if invasion_strength > total_defense_power and bots_broken > 0:
        lost_gold = min(player.gold, (total_defense_power - invasion_strength) * random.randrange(5, 20))
        player.gold = lost_gold
        print(f"Your defenses failed! Gold stolen: -{lost_gold}")

    return bots_broken
