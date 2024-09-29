import unittest
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
        
if __name__ == '__main__':
    unittest.main()
