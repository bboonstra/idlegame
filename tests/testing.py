import unittest
import unittest.mock
from idlegame.nanobots import Nanobot, Nanotype
from idlegame.data import save, load, AutosavedPlayer
from idlegame.battle import simulate_defense
from idlegame.packages import install_package, is_package_installed
from idlegame.idle import handle_claim
from idlegame.main import CommandLineInterface
from io import StringIO
import sys
import os
import tempfile
from datetime import datetime, timezone, timedelta

class TestNanobots(unittest.TestCase):
    
    def setUp(self):
        self.nb = Nanobot("testbot", "idle mine\non invasion defend", Nanotype.NORMAL)
    
    def test_setup(self):
        self.assertEqual(self.nb.name, "testbot")
    
    def test_scripting(self):
        self.assertEqual(self.nb.idle_action, "mine")
        self.assertEqual(self.nb.event_actions["invasion"], "defend")
    
    def test_nanobot_types(self):
        miner = Nanobot("miner", "idle mine", Nanotype.MINER)
        fighter = Nanobot("fighter", "idle defend", Nanotype.FIGHTER)
        self.assertGreater(miner.mining_rate, 1)
        self.assertGreater(fighter.defense_rating, 1)

class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for saving and loading data."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
        self.temp_file.close()  # Close the file so it can be used by save/load
        self.tdata = {"this is a ": "test"}

    def tearDown(self):
        """Clean up the temporary file after tests."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_save(self):
        """Test that saving correctly stores data."""
        save(self.tdata, self.temp_file.name)  # Pass the temp file path to save
        
        # Verify that the file exists
        self.assertTrue(os.path.exists(self.temp_file.name), "The pickle file does not exist.")

    def test_load(self):
        """Test that load correctly loads data."""
        save(self.tdata, self.temp_file.name)  # Save the data first
        loaded_data = load(self.temp_file.name)  # Load it back
        
        # Assert the loaded data matches
        self.assertEqual(loaded_data, self.tdata, "Loaded data does not match the saved data.")

    def test_load_nonexistent_file(self):
        """Test loading from a non-existent file."""
        non_existent_file = "non_existent_file.pkl"
        loaded_data = load(non_existent_file)
        self.assertEqual(loaded_data, {}, "Loading non-existent file should return an empty dict.")

class TestCommandLineInterface(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh AutosavedPlayer instance and CommandLineInterface before each test."""
        self.player = AutosavedPlayer()  # Create an instance of your player class
        self.cli = CommandLineInterface(self.player)  # Create an instance of your CLI

    def redirect_stdout(self, func, *args, **kwargs):
        """Helper method to capture stdout during a function call."""
        output = StringIO()
        sys.stdout = output
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = sys.__stdout__  # Reset redirect
        return output.getvalue().strip()

    def test_handle_man_sudo(self):
        """Test that handle_man correctly prints 'No manual entry for sudo'."""
        output = self.redirect_stdout(self.cli.handle_man, self.player, "sudo")
        self.assertEqual(output, "No manual entry for sudo")  # Assert the output is as expected

    def test_alias_refusal(self):
        """Test that invalid aliases are correctly refused."""
        self.player.aliases['a'] = 'goob'
        output = self.redirect_stdout(self.cli.default, "a")
        self.assertEqual(output, "Your alias is set to 'goob', but that is not a valid command.")  # Assert the output is as expected
        del self.player.aliases['a']

    def test_packages(self):
        """Test that invalid aliases are correctly refused."""
        self.player.packages = []
        output = self.redirect_stdout(self.cli.default, "apt")
        self.assertEqual(output, "apt has not been installed!", "apt should not be installed by default.")

        # Mock user input for the 'apt' command
        self.player.packages = ['apt']
        with unittest.mock.patch('builtins.input', side_effect=["yum"]):  # Simulate input here
            output = self.redirect_stdout(self.cli.default, "apt")

        self.assertTrue(output.startswith("Available packages to install:"), "apt should work when installed.")

    def test_handle_top(self):
        """Test the 'top' command output."""
        self.player.nanobots.append(Nanobot("bot1", "idle mine", Nanotype.NORMAL))
        self.player.nanobots.append(Nanobot("bot2", "idle defend", Nanotype.FIGHTER))
        output = self.redirect_stdout(self.cli.handle_top, self.player)
        self.assertIn("System complexity:", output)
        self.assertIn("Safety level:", output)

    def test_handle_alias(self):
        """Test setting and displaying aliases."""
        # Set an alias
        self.cli.handle_alias(self.player, "m", "man")
        self.assertIn("m", self.player.aliases)
        self.assertEqual(self.player.aliases["m"], "man")

        # Display aliases
        output = self.redirect_stdout(self.cli.handle_alias, self.player)
        self.assertIn("m -> man", output)

class TestBattle(unittest.TestCase):
    def setUp(self):
        self.player = AutosavedPlayer()
        self.player.nanobots = [
            Nanobot("defender1", "idle defend", Nanotype.FIGHTER),
            Nanobot("defender2", "idle defend", Nanotype.NORMAL)
        ]

    def test_simulate_defense(self):
        broken_bots = simulate_defense(self.player, self.player.nanobots)
        self.assertIsInstance(broken_bots, int)
        self.assertGreaterEqual(broken_bots, 0)
        self.assertLessEqual(broken_bots, len(self.player.nanobots))

class TestPackages(unittest.TestCase):
    def setUp(self):
        self.player = AutosavedPlayer()

    def test_install_package(self):
        self.player.gold = 1000
        install_package(self.player, 'apt')
        self.assertTrue(is_package_installed(self.player, 'apt'))

    def test_install_package_insufficient_funds(self):
        self.player.gold = 0
        install_package(self.player, 'yum')
        self.assertFalse(is_package_installed(self.player, 'yum'))

class TestIdle(unittest.TestCase):
    def setUp(self):
        self.player = AutosavedPlayer()
        self.player.nanobots = [
            Nanobot("miner", "idle mine", Nanotype.MINER),
            Nanobot("defender", "idle defend", Nanotype.FIGHTER)
        ]
        self.player.last_claim_timestamp = datetime.now(timezone.utc) - timedelta(hours=1)

    def test_handle_claim(self):
        initial_gold = self.player.gold
        handle_claim(self.player)
        self.assertGreater(self.player.gold, initial_gold)

class TestComplexity(unittest.TestCase):
    def setUp(self):
        """Set up a fresh player instance."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
        self.temp_file.close()  # Close the file so it can be used by save/load
        self.player = AutosavedPlayer()  # Create an instance of your player class
        self.player._data = self.player.DEFAULT_ATTRIBUTES.copy()
        save(self.player._data, self.temp_file.name)
        self.player = AutosavedPlayer(self.temp_file.name)

    def tearDown(self):
        """Clean up the temporary file after tests."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_complexity_updates(self):
        """Test that the complexity of the system updates when a bot is added."""
        self.assertEqual(self.player.system_complexity, 0.0, "System complexity should be 0 by default.")

        self.player.nanobots.append(Nanobot("testbot", "1234567890", Nanotype.NORMAL))
        self.player.update_complexity()  # Call a method to update complexity after adding a bot

        self.assertEqual(self.player.system_complexity, 1.0, "System complexity should be 1 with a bot with len(10) of code.")

    def test_complexity_with_aliases(self):
        """Test that aliases contribute to system complexity."""
        self.player.update_complexity()
        initial_complexity = self.player.system_complexity
        self.player.aliases['test_alias'] = 'some_command'
        self.player.update_complexity()
        self.assertGreater(self.player.system_complexity, initial_complexity)

if __name__ == '__main__':
    unittest.main()