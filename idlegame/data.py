import os
import pickle
import getpass
import config

def load(filename: str = config.save_file) -> dict:
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}

def save(data: dict, filename: str = config.save_file) -> None:
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

class AutosavedPlayer:
    DEFAULT_ATTRIBUTES: dict[str, int, dict] = {
        'hp': 100,
        'level': 1,
        'experience': 0,
        'gold': 0,
        'last_claim_timestamp': None,
        'settings': {},
        'aliases': {},
    }

    def __init__(self) -> None:
        self.username = getpass.getuser()  # Automatically use the current system user
        self._data = self.load()
        self.automigrate()

        for key, value in self._data.items():
            setattr(self, key, value)

    def load(self, filename: str = config.save_file) -> dict:
        if os.path.exists(filename):
            data = pickle.load(open(filename, 'rb'))
            return data
        print("Welcome to idlegame, the pip & play Python game!")
        print("idlegame emulates a zsh command line to play. Get started: `man idlegame` / `man commands`")
        print("© 2024 Ben Boonstra MIT License.")
        return {}

    def save(self, filename: str = config.save_file) -> None:
        save(self._data)

    def __getattr__(self, attr: str) -> int:
        if attr in self._data:
            return self._data[attr]
        raise AttributeError(f"{attr} not found")

    def __setattr__(self, attr: str, value: int) -> None:
        if attr in ['username', '_data']:
            super().__setattr__(attr, value)
        else:
            self._data[attr] = value
            self.save()

    def automigrate(self) -> None:
        for attr, default_value in self.DEFAULT_ATTRIBUTES.items():
            if attr not in self._data:
                self._data[attr] = default_value

def handle_login() -> AutosavedPlayer:
    """Automatically login as the current system user."""
    username = getpass.getuser()
    print(f"Logged in as: {username}")

    return AutosavedPlayer()