import unittest
from idlegame.data import AutosavedPlayer

class TestAutosavedPlayer(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh AutosavedPlayer instance before each test."""
        self.player = AutosavedPlayer()
    
    def test_initial_gold(self):
        """Test that a new player starts with 0 gold."""
        self.assertEqual(self.player.gold, 0)
    
    def test_add_gold(self):
        """Test adding gold to the player."""
        self.player.gold += 50
        self.assertEqual(self.player.gold, 50)
    
    # Add more tests here for other functionalities

if __name__ == '__main__':
    unittest.main()
