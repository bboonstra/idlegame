from datetime import timedelta

save_file = 'savedata.pickle'
disallowed_usernames = ['cancel']
base_mining_rate = 1
sim_chunk_duration = 600 # 600 seconds = 10 minutes
invasion_chance_per_chunk = 0.05 # 5% per 10 mins

def handle_sudo(player, *args, **kwargs):
    key = kwargs.get('k', '')
    if key.lower() != "verysecure":
        print("Invalid command. Try 'man commands'!")
        return

    ts = kwargs.get('lengthen-uptime', 0)

    if ts:
        # Subtract the specified number of seconds from the last claim timestamp
        player.last_claim_timestamp -= timedelta(seconds=int(ts))
        print(f"Added {int(ts)/60} mins to uptime")
    

