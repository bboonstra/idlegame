import unittest
import unittest.mock
from idlegame.nanobots import Nanobot, Nanotype
from idlegame.data import save, load, AutosavedPlayer
from io import StringIO
import sys
import os
import tempfile
from idlegame.main import CommandLineInterface

class TestNanobots(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh AutosavedPlayer instance before each test."""
        self.nb = Nanobot("testbot", "idle mine", Nanotype.NORMAL)
    
    def test_setup(self):
        """Test that a the Nanobot was setup properly."""
        self.assertEqual(self.nb.name, "testbot")
    
    def test_scripting(self):
        """Test that the scripting was correctly interpreted."""
        self.assertEqual(self.nb.idle_action, "mine")

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

        self.player.nanos.append(Nanobot("testbot", "1234567890", Nanotype.NORMAL))
        self.player.update_complexity()  # Call a method to update complexity after adding a bot

        self.assertEqual(self.player.system_complexity, 1.0, "System complexity should be 1 with a bot with len(10) of code.")

if __name__ == '__main__':
    unittest.main()
