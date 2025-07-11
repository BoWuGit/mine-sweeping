"""
Unit tests for the game logic module.
"""
import pytest
from unittest.mock import patch
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.game_logic import MinesweeperGame, GameManager
from app.models import CellState, GameStatus, Difficulty


class TestMinesweeperGame:
    """Test cases for MinesweeperGame class."""
    
    def test_game_initialization(self):
        """Test game initialization with correct parameters."""
        game = MinesweeperGame(10, 10, 10)
        
        assert game.width == 10
        assert game.height == 10
        assert game.mine_count == 10
        assert game.status == GameStatus.PLAYING
        assert game.revealed_count == 0
        assert game.flagged_count == 0
        assert len(game.board) == 10
        assert len(game.board[0]) == 10
    
    def test_board_creation(self):
        """Test that board is created with correct structure."""
        game = MinesweeperGame(5, 5, 5)
        
        # Check board dimensions
        assert len(game.board) == 5
        assert len(game.board[0]) == 5
        
        # Check all cells are hidden initially
        for row in game.board:
            for cell in row:
                assert cell.state == CellState.HIDDEN
                assert not cell.is_mine
                assert cell.neighbor_mines == 0
                assert not cell.is_revealed
    
    def test_mine_placement(self):
        """Test that mines are placed correctly on first click."""
        game = MinesweeperGame(5, 5, 3)
        
        # First click should place mines
        game.reveal_cell(0, 0)
        
        assert game.mines_placed
        assert game.revealed_count > 0
        
        # Count actual mines
        mine_count = sum(1 for row in game.board for cell in row if cell.is_mine)
        assert mine_count == 3
    
    def test_first_click_safety(self):
        """Test that first click is always safe."""
        game = MinesweeperGame(5, 5, 24)  # Almost all cells are mines
        
        # First click should be safe
        result = game.reveal_cell(0, 0)
        assert result  # Game should continue
        assert not game.board[0][0].is_mine
    
    def test_cell_reveal(self):
        """Test revealing cells."""
        game = MinesweeperGame(5, 5, 3)
        
        # Reveal a cell
        result = game.reveal_cell(0, 0)
        assert result
        assert game.board[0][0].state == CellState.REVEALED
        assert game.board[0][0].is_revealed
    
    def test_mine_explosion(self):
        """Test hitting a mine."""
        game = MinesweeperGame(5, 5, 3)
        
        # Place mines first
        game.reveal_cell(0, 0)
        
        # Find a mine and click it
        mine_found = False
        for y in range(5):
            for x in range(5):
                if game.board[y][x].is_mine:
                    result = game.reveal_cell(x, y)
                    assert not result  # Game should end
                    assert game.status == GameStatus.LOST
                    assert game.board[y][x].state == CellState.EXPLODED
                    mine_found = True
                    break
            if mine_found:
                break
        
        assert mine_found
    
    def test_flag_toggle(self):
        """Test flagging and unflagging cells."""
        game = MinesweeperGame(5, 5, 3)
        
        # Flag a cell
        result = game.flag_cell(0, 0)
        assert result
        assert game.board[0][0].state == CellState.FLAGGED
        assert game.flagged_count == 1
        
        # Unflag the cell
        result = game.flag_cell(0, 0)
        assert result
        assert game.board[0][0].state == CellState.HIDDEN
        assert game.flagged_count == 0
    
    def test_cannot_flag_revealed_cell(self):
        """Test that revealed cells cannot be flagged."""
        game = MinesweeperGame(5, 5, 3)
        
        # Reveal a cell
        game.reveal_cell(0, 0)
        
        # Try to flag it
        result = game.flag_cell(0, 0)
        assert not result
    
    def test_cannot_reveal_flagged_cell(self):
        """Test that flagged cells cannot be revealed."""
        game = MinesweeperGame(5, 5, 3)
        
        # Flag a cell
        game.flag_cell(0, 0)
        
        # Try to reveal it
        result = game.reveal_cell(0, 0)
        assert result  # Should not reveal, but game continues
        assert game.board[0][0].state == CellState.FLAGGED
    
    def test_win_condition(self):
        """Test win condition."""
        # Create a game with only one mine
        game = MinesweeperGame(3, 3, 1)
        
        # Place the mine at (0, 0)
        with patch.object(game, '_place_mines') as mock_place:
            def place_mines_side_effect(x, y):
                game.board[0][0].is_mine = True
                game.mines_placed = True
                game._calculate_neighbor_mines()
            
            mock_place.side_effect = place_mines_side_effect
            
            # Reveal all non-mine cells
            for y in range(3):
                for x in range(3):
                    if x != 0 or y != 0:  # Skip the mine
                        game.reveal_cell(x, y)
            
            assert game.status == GameStatus.WON
    
    def test_invalid_coordinates(self):
        """Test handling of invalid coordinates."""
        game = MinesweeperGame(5, 5, 3)
        
        # Try invalid coordinates
        result = game.reveal_cell(-1, 0)
        assert result  # Should handle gracefully
        
        result = game.reveal_cell(10, 0)
        assert result  # Should handle gracefully
        
        result = game.flag_cell(0, -1)
        assert not result
        
        result = game.flag_cell(0, 10)
        assert not result
    
    def test_neighbor_mine_calculation(self):
        """Test neighbor mine count calculation."""
        game = MinesweeperGame(3, 3, 3)
        
        # Manually place mines in corners
        game.board[0][0].is_mine = True
        game.board[0][2].is_mine = True
        game.board[2][0].is_mine = True
        
        game._calculate_neighbor_mines()
        
        # Center cell should have 3 neighbors
        assert game.board[1][1].neighbor_mines == 3
        
        # Edge cells should have appropriate counts
        assert game.board[0][1].neighbor_mines == 2
        assert game.board[1][0].neighbor_mines == 2


class TestGameManager:
    """Test cases for GameManager class."""
    
    def test_create_game(self):
        """Test creating a new game."""
        manager = GameManager()
        
        game_id = manager.create_game(Difficulty.EASY, 10, 10, 10)
        assert game_id is not None
        
        game = manager.get_game(game_id)
        assert game is not None
        assert game.width == 10
        assert game.height == 10
        assert game.mine_count == 10
    
    def test_get_nonexistent_game(self):
        """Test getting a game that doesn't exist."""
        manager = GameManager()
        
        game = manager.get_game("nonexistent")
        assert game is None
    
    def test_delete_game(self):
        """Test deleting a game."""
        manager = GameManager()
        
        game_id = manager.create_game(Difficulty.EASY, 10, 10, 10)
        assert manager.get_game(game_id) is not None
        
        success = manager.delete_game(game_id)
        assert success
        assert manager.get_game(game_id) is None
    
    def test_delete_nonexistent_game(self):
        """Test deleting a game that doesn't exist."""
        manager = GameManager()
        
        success = manager.delete_game("nonexistent")
        assert not success
    
    def test_list_games(self):
        """Test listing all games."""
        manager = GameManager()
        
        # Create multiple games
        game_id1 = manager.create_game(Difficulty.EASY, 10, 10, 10)
        game_id2 = manager.create_game(Difficulty.MEDIUM, 16, 16, 40)
        
        games = manager.list_games()
        assert len(games) == 2
        
        game_ids = [game.game_id for game in games]
        assert game_id1 in game_ids
        assert game_id2 in game_ids
    
    def test_difficulty_configs(self):
        """Test predefined difficulty configurations."""
        manager = GameManager()
        
        # Test easy difficulty
        game_id = manager.create_game(Difficulty.EASY)
        game = manager.get_game(game_id)
        assert game.width == 10
        assert game.height == 10
        assert game.mine_count == 10
        
        # Test medium difficulty
        game_id = manager.create_game(Difficulty.MEDIUM)
        game = manager.get_game(game_id)
        assert game.width == 16
        assert game.height == 16
        assert game.mine_count == 40
        
        # Test hard difficulty
        game_id = manager.create_game(Difficulty.HARD)
        game = manager.get_game(game_id)
        assert game.width == 16
        assert game.height == 30
        assert game.mine_count == 99


if __name__ == "__main__":
    pytest.main([__file__]) 