"""
Test flag-based win condition for Minesweeper game.
"""
import pytest
from app.game_logic import MinesweeperGame, GameStatus, CellState


class TestFlagWinCondition:
    """Test cases for flag-based win condition."""
    
    def setup_method(self):
        """Set up a test game with mines at specific positions."""
        # Create a small game for testing
        self.game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        self.game.board[0][0].is_mine = True  # (0,0)
        self.game.board[1][0].is_mine = True  # (0,1)
        self.game.mines_placed = True
        self.game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        self.game.status = GameStatus.PLAYING
    
    def test_flag_all_mines_win(self):
        """Test that flagging all mines results in a win."""
        # Flag the first mine
        result = self.game.flag_cell(0, 0)
        assert result is True
        assert self.game.flagged_count == 1
        assert self.game.status == GameStatus.PLAYING
        
        # Flag the second mine
        result = self.game.flag_cell(0, 1)
        assert result is True
        assert self.game.flagged_count == 2
        assert self.game.status == GameStatus.WON
    
    def test_flag_wrong_cells_no_win(self):
        """Test that flagging wrong cells doesn't result in a win."""
        # Flag wrong cells (not mines)
        result = self.game.flag_cell(1, 1)
        assert result is True
        assert self.game.flagged_count == 1
        assert self.game.status == GameStatus.PLAYING
        
        result = self.game.flag_cell(2, 2)
        assert result is True
        assert self.game.flagged_count == 2
        # Should not win because we flagged wrong cells
        assert self.game.status == GameStatus.PLAYING
    
    def test_mixed_flag_and_reveal_win(self):
        """Test win condition with both flagging and revealing."""
        # Flag one mine
        result = self.game.flag_cell(0, 0)
        assert result is True
        assert self.game.flagged_count == 1
        assert self.game.status == GameStatus.PLAYING
        
        # Reveal all non-mine cells
        for y in range(3):
            for x in range(3):
                if not self.game.board[y][x].is_mine and self.game.board[y][x].state != CellState.FLAGGED:
                    self.game.reveal_cell(x, y)
        
        # Should win by revealing all safe cells
        assert self.game.status == GameStatus.WON
    
    def test_win_condition_verification(self):
        """Test that win condition correctly verifies flagged mines."""
        # Flag one mine and one non-mine
        self.game.flag_cell(0, 0)  # Correct mine
        self.game.flag_cell(1, 1)  # Wrong cell (not a mine)
        
        # Should not win because we flagged a wrong cell
        assert self.game.status == GameStatus.PLAYING
        
        # Unflag wrong cell and flag correct mine
        self.game.flag_cell(1, 1)  # Unflag wrong cell
        self.game.flag_cell(0, 1)  # Flag correct mine
        
        # Should win now
        assert self.game.status == GameStatus.WON 