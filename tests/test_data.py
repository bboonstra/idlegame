import unittest
from idlegame.nanobots import Nanobot, Nanotype

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

if __name__ == '__main__':
    unittest.main()
