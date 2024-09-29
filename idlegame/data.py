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

def update(username: str, user_data: dict, filename: str = config.save_file) -> None:
    """Update the data for a specific user."""
    all_data = load(filename)  # Load existing data
    if username in all_data:
        all_data[username].update(user_data)  # Update user data
    else:
        all_data[username] = user_data  # If user doesn't exist, create new entry
    save(all_data)  # Save the updated data

def delete(username: str) -> None:
    """Delete a user by username."""
    user_data = load()
    if username in user_data:
        del user_data[username]
        save(user_data)
        print(f"User '{username}' has been deleted.")
    else:
        print(f"User '{username}' not found.")

class AutosavedPlayer:
    DEFAULT_ATTRIBUTES: dict[str, int] = {
        'hp': 100,
        'level': 1,
        'experience': 0,
        'gold': 0,
        'last_claim_timestamp': None,
    }

    def __init__(self, username: str) -> None:
        self.username = username
        self._data = self.load()
        self.automigrate()

        for key, value in self._data.items():
            setattr(self, key, value)

    def load(self, filename: str = config.save_file) -> dict:
        if os.path.exists(filename):
            all_data = pickle.load(open(filename, 'rb'))
            return all_data.get(self.username, {})
        return {}

    def save(self, filename: str = config.save_file) -> None:
        all_data = load(filename)
        all_data[self.username] = self._data
        save(all_data)

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
    user_data = load()

    while True:  # Loop until a valid choice is made
        if not user_data:
            default_username = getpass.getuser()
            username = input(f"No users found. Press enter to start as {default_username}, or type in a name: ") or default_username
            
            if username in config.disallowed_usernames:
                print("That username is not allowed. Please choose a different name.")
                continue

            user_data[username] = {}
            save(user_data)
            print(f"Welcome, {username}! Your data has been saved.")
            return AutosavedPlayer(username)
        else:
            print("Select a user:")
            for index, user in enumerate(user_data.keys(), start=1):
                print(f"{index}. {user}")

            print(f"{len(user_data) + 1}. Create a new user")
            print(f"{len(user_data) + 2}. Delete a user")

            choice = input("Choose an option (number): ")

            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(user_data):
                    selected_username = list(user_data.keys())[choice - 1]
                    print(f"Welcome back, {selected_username}!")
                    return AutosavedPlayer(selected_username)
                elif choice == len(user_data) + 1:
                    default_username = getpass.getuser()
                    new_username = input(f"Press enter to start as {default_username}, or type in a name: ") or default_username
                    user_data[new_username] = {}
                    save(user_data)
                    print(f"Welcome, {new_username}! Your data has been saved.")
                    return AutosavedPlayer(new_username)
                elif choice == len(user_data) + 2:
                    # Delete a user
                    delete_username = input("Enter the username to delete or type 'cancel' to cancel: ")
                    if delete_username == 'cancel':
                        print("User deletion cancelled.")
                    elif delete_username in user_data:
                        confirm = input(f"Are you sure you want to delete the user '{delete_username}'? (yes/no): ")
                        if confirm.lower() == 'yes':
                            del user_data[delete_username]
                            save(user_data)
                            print(f"User '{delete_username}' has been deleted.")
                        else:
                            print("User deletion cancelled.")
                    else:
                        print("Username not found. Please try again.")
            else:
                print("Invalid choice. Please try again.")