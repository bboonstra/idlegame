from typing import List, Dict
from idlegame.config import core_rarities
from idlegame.data import AutosavedPlayer
from idlegame.nanobots import Nanobot, Nanotype
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
        
        # Warper ability: chance to "warp" and double defense power
        if bot.type == Nanotype.WARPER and random.random() < bot.warp_chance:
            total_defense_power += bot.defense_rating
            print(f"{bot.name} warped and doubled its defense power!")

    # Simulate the invasion strength
    invasion_strength = max(round((random.random() + 0.1) * (player.system_complexity - 3)), 0)
    print(f"Invasion strength: {invasion_strength}, Total defense power: {total_defense_power}")

    # Calculate the ratio of defense power to invasion strength
    defense_ratio = total_defense_power / invasion_strength if invasion_strength > 0 else 1

    # Determine the chance of breaking bots based on defense ratio
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

    # Determine core rewards based on invasion strength and defense success
    if invasion_strength > 0 and total_defense_power >= invasion_strength:
        core_rewards = determine_core_rewards(invasion_strength)
        for core_type, amount in core_rewards.items():
            player.nano_cores[core_type] += amount
            if amount > 0:
                print(f"Your successful defense earned you {amount} {core_type} core(s)!")

    if bots_broken == 0:
        print(f"Your defenses held against an invasion (Strength: {invasion_strength}).")

    if invasion_strength > total_defense_power and bots_broken > 0:
        lost_gold = min(player.gold, (invasion_strength - total_defense_power) * random.randrange(5, 20))
        player.gold -= lost_gold
        print(f"Your defenses failed! Gold stolen: -{lost_gold}")

    return bots_broken

def determine_core_rewards(power: int) -> Dict[str, int]:
    """Determine the core rewards based on the remaining power after defense."""
    rewards = {core_type: 0 for core_type in core_rarities.keys()}
    
    while power > 0:
        possible_cores = [core for core, rarity in core_rarities.items() if rarity <= power]
        if not possible_cores:
            break
        
        chosen_core = random.choice(possible_cores)
        rewards[chosen_core] += 1
        power -= core_rarities[chosen_core]
    
    return rewards
