"""
Test flag-based win condition for Minesweeper game.
"""
import pytest
from app.game_logic import MinesweeperGame, GameStatus, CellState


class TestFlagWinCondition:
    """Test cases for flag-based win condition."""
    
    def test_flag_all_mines_win(self):
        """Test that flagging all mines results in a win."""
        # Create a small game for testing
        game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        game.board[0][0].is_mine = True
        game.board[0][1].is_mine = True
        game.mines_placed = True
        game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        game.status = GameStatus.PLAYING
        
        # Flag the first mine
        result = game.flag_cell(0, 0)
        assert result is True
        assert game.flagged_count == 1
        assert game.status == GameStatus.PLAYING
        
        # Flag the second mine
        result = game.flag_cell(0, 1)
        assert result is True
        assert game.flagged_count == 2
        assert game.status == GameStatus.WON
    
    def test_flag_wrong_cells_no_win(self):
        """Test that flagging wrong cells doesn't result in a win."""
        # Create a small game for testing
        game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        game.board[0][0].is_mine = True
        game.board[0][1].is_mine = True
        game.mines_placed = True
        game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        game.status = GameStatus.PLAYING
        
        # Flag wrong cells (not mines)
        result = game.flag_cell(1, 1)
        assert result is True
        assert game.flagged_count == 1
        assert game.status == GameStatus.PLAYING
        
        result = game.flag_cell(2, 2)
        assert result is True
        assert game.flagged_count == 2
        # Should not win because we flagged wrong cells
        assert game.status == GameStatus.PLAYING
    
    def test_mixed_flag_and_reveal_win(self):
        """Test win condition with both flagging and revealing."""
        # Create a small game for testing
        game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        game.board[0][0].is_mine = True
        game.board[0][1].is_mine = True
        game.mines_placed = True
        game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        game.status = GameStatus.PLAYING
        
        # Flag one mine
        result = game.flag_cell(0, 0)
        assert result is True
        assert game.flagged_count == 1
        assert game.status == GameStatus.PLAYING
        
        # Reveal all non-mine cells
        for y in range(3):
            for x in range(3):
                if not game.board[y][x].is_mine and game.board[y][x].state != CellState.FLAGGED:
                    game.reveal_cell(x, y)
        
        # Should win by revealing all safe cells
        assert game.status == GameStatus.WON
    
    def test_flag_then_unflag_no_win(self):
        """Test that unflagging a mine removes the win condition."""
        # Create a small game for testing
        game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        game.board[0][0].is_mine = True
        game.board[0][1].is_mine = True
        game.mines_placed = True
        game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        game.status = GameStatus.PLAYING
        
        # Flag both mines
        game.flag_cell(0, 0)
        game.flag_cell(0, 1)
        assert game.status == GameStatus.WON
        
        # Unflag one mine
        game.flag_cell(0, 0)
        assert game.status == GameStatus.PLAYING
    
    def test_win_condition_verification(self):
        """Test that win condition correctly verifies flagged mines."""
        # Create a small game for testing
        game = MinesweeperGame(width=3, height=3, mine_count=2)
        
        # Manually place mines at specific positions for testing
        game.board[0][0].is_mine = True
        game.board[0][1].is_mine = True
        game.mines_placed = True
        game._calculate_neighbor_mines()
        
        # Ensure the game is in playing state
        game.status = GameStatus.PLAYING
        
        # Flag one mine and one non-mine
        game.flag_cell(0, 0)  # Correct mine
        game.flag_cell(1, 1)  # Wrong cell (not a mine)
        
        # Should not win because we flagged a wrong cell
        assert game.status == GameStatus.PLAYING
        
        # Unflag wrong cell and flag correct mine
        game.flag_cell(1, 1)  # Unflag wrong cell
        game.flag_cell(0, 1)  # Flag correct mine
        
        # Should win now
        assert game.status == GameStatus.WON 