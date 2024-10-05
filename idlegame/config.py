from datetime import timedelta

save_file = 'idlegame-savedata.pickle'
disallowed_usernames = ['cancel']
base_mining_rate = 1
sim_chunk_duration = 600 # 600 seconds = 10 minutes
invasion_chance_per_chunk = 0.05 # 5% per 10 mins
fsck_cost = 100.0

shop_items = {
    'Normal Nanocore': {'description': 'Get a normal nanocore!', 'price_gold': 100, 'reward': 'normal nanocore'},
    'Miner Nanocore': {'description': 'Get a miner nanocore!', 'price_gold': 500, 'reward': 'miner nanocore'},
    'Fighter Nanocore': {'description': 'Get a fighter nanocore!', 'price_gold': 750, 'reward': 'fighter nanocore'},
    'Super Nanocore': {'description': 'Get a super nanocore!', 'price_gold': 1500, 'reward': 'super nanocore'},
    'Warper Nanocore': {'description': 'Get a warper nanocore!', 'price_gold': 5000, 'reward': 'warper nanocore'},
    'Time Crystal': {'description': 'A mysterious crystal that bends time', 'price_gold': 10000, 'reward': 'time_crystal'},
    'Researcher Nanocore': {'description': 'Get a researcher nanocore!', 'price_gold': 2000, 'reward': 'researcher nanocore'},
    'Hacker Nanocore': {'description': 'Get a hacker nanocore!', 'price_gold': 3000, 'reward': 'hacker nanocore'},
    'Diplomat Nanocore': {'description': 'Get a diplomat nanocore!', 'price_gold': 2500, 'reward': 'diplomat nanocore'},
}

shop_cooldown_hours = 24 # the shop rerolls once per day

core_rarities = {
    'normal': 10,
    'miner': 25,
    'fighter': 40,
    'super': 70,
    'warper': 100,
    'researcher': 60,
    'hacker': 80,
    'diplomat': 70
}

def handle_sudo(player, *args, **kwargs):
    # Good job, you found the secret sudo function! Use it, I don't care lol
    key = kwargs.get('k', '')
    if key.lower() != "lol":
        print("Invalid command. Try 'man'!")
        return

    ts = kwargs.get('lengthen-uptime', 0)
    if not ts:
        ts = kwargs.get('lup', 0)
    if ts:
        # Subtract the specified number of seconds from the last claim timestamp
        player.last_claim_timestamp -= timedelta(seconds=int(ts))
        print(f"Added {int(ts)/60} mins to uptime")

    gold = kwargs.get('add-gold', 0)
    if not gold:
        gold = kwargs.get('ag', 0)
    if gold:
        # Subtract the specified number of seconds from the last claim timestamp
        player.gold += int(gold)
        print(f"Added {gold} gold to your account")

    cores = kwargs.get('add-normal-nanocores', 0)
    if not cores:
        cores = kwargs.get('anc', 0)
    if cores:
        player.nano_cores['normal'] += int(cores)
        print(f"Added {cores} normal cores to your account")
