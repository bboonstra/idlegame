from datetime import timedelta

save_file = 'idlegame-savedata.pickle'
disallowed_usernames = ['cancel']
base_mining_rate = 1
sim_chunk_duration = 600 # 600 seconds = 10 minutes
invasion_chance_per_chunk = 0.05 # 5% per 10 mins
fsck_cost = 100.0
def handle_sudo(player, *args, **kwargs):
    # Good job, you found the secret sudo function! Use it, I don't care lol
    key = kwargs.get('k', '')
    if key.lower() != "lol":
        print("Invalid command. Try 'man commands'!")
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
