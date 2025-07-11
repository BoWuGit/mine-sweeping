"""
Core game logic for the Minesweeper game.
"""
import random
from typing import List, Tuple, Set
from datetime import datetime
import uuid

from .models import (
    Cell, CellState, GameStatus, GameState, 
    Difficulty, DIFFICULTY_CONFIGS
)


class MinesweeperGame:
    """Core game logic for Minesweeper."""
    
    def __init__(self, width: int, height: int, mine_count: int):
        """
        Initialize a new Minesweeper game.
        
        Args:
            width: Board width
            height: Board height
            mine_count: Number of mines to place
        """
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.game_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        
        # Initialize board
        self.board = self._create_empty_board()
        self.mines_placed = False
        self.status = GameStatus.PLAYING
        self.revealed_count = 0
        self.flagged_count = 0
        
    def _create_empty_board(self) -> List[List[Cell]]:
        """Create an empty board with all cells hidden."""
        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(
                    x=x,
                    y=y,
                    state=CellState.HIDDEN,
                    is_mine=False,
                    neighbor_mines=0,
                    is_revealed=False
                )
                row.append(cell)
            board.append(row)
        return board
    
    def _place_mines(self, first_x: int, first_y: int):
        """
        Place mines on the board, ensuring the first clicked cell is safe.
        
        Args:
            first_x: X coordinate of first click
            first_y: Y coordinate of first click
        """
        if self.mines_placed:
            return
            
        # Create list of all possible positions
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if x != first_x or y != first_y:
                    positions.append((x, y))
        
        # Randomly select mine positions
        mine_positions = random.sample(positions, self.mine_count)
        
        # Place mines
        for x, y in mine_positions:
            self.board[y][x].is_mine = True
        
        # Calculate neighbor mine counts
        self._calculate_neighbor_mines()
        self.mines_placed = True
    
    def _calculate_neighbor_mines(self):
        """Calculate the number of mines in adjacent cells for each cell."""
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.width and 
                                0 <= ny < self.height and 
                                self.board[ny][nx].is_mine):
                                count += 1
                    self.board[y][x].neighbor_mines = count
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get all valid neighbor coordinates for a cell."""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors
    
    def reveal_cell(self, x: int, y: int) -> bool:
        """
        Reveal a cell at the given coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the game should continue, False if game over
        """
        if self.status != GameStatus.PLAYING:
            return False
            
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True  # Return True to handle gracefully
            
        cell = self.board[y][x]
        
        # Don't reveal flagged cells
        if cell.state == CellState.FLAGGED:
            return True
            
        # Don't reveal already revealed cells
        if cell.state == CellState.REVEALED:
            return True
        
        # Place mines on first click if not already placed
        if not self.mines_placed:
            self._place_mines(x, y)
        
        # Check if clicked on mine
        if cell.is_mine:
            cell.state = CellState.EXPLODED
            self.status = GameStatus.LOST
            self.last_updated = datetime.now()
            return False
        
        # Reveal the cell
        self._reveal_cell_recursive(x, y)
        self.last_updated = datetime.now()
        
        # Check for win condition
        if self._check_win_condition():
            self.status = GameStatus.WON
            
        return True
    
    def _reveal_cell_recursive(self, x: int, y: int):
        """
        Recursively reveal cells using flood fill algorithm.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        cell = self.board[y][x]
        
        # Don't reveal flagged or already revealed cells
        if cell.state in [CellState.FLAGGED, CellState.REVEALED]:
            return
        
        # Reveal this cell
        cell.state = CellState.REVEALED
        cell.is_revealed = True
        self.revealed_count += 1
        
        # If no neighboring mines, reveal neighbors
        if cell.neighbor_mines == 0:
            for nx, ny in self._get_neighbors(x, y):
                self._reveal_cell_recursive(nx, ny)
    
    def flag_cell(self, x: int, y: int) -> bool:
        """
        Toggle flag on a cell.
        Only allowed when game is PLAYING.
        """
        if self.status != GameStatus.PLAYING:
            return False
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        cell = self.board[y][x]
        # Don't flag revealed cells
        if cell.state == CellState.REVEALED:
            return False
        # Toggle flag
        if cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
            self.flagged_count -= 1
        else:
            cell.state = CellState.FLAGGED
            self.flagged_count += 1
        self.last_updated = datetime.now()
        # Check for win condition after flagging
        if self._check_win_condition():
            self.status = GameStatus.WON
        return True

    def _check_win_condition(self) -> bool:
        """Check if the player has won the game."""
        total_cells = self.width * self.height
        # 1. 所有非地雷格子都被揭开
        all_safe_cells_revealed = self.revealed_count == (total_cells - self.mine_count)
        # 2. 所有地雷都被正确标记，且没有多余标记
        flagged_mines = 0
        flagged_non_mines = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell.state == CellState.FLAGGED:
                    if cell.is_mine:
                        flagged_mines += 1
                    else:
                        flagged_non_mines += 1
        all_mines_flagged = (
            flagged_mines == self.mine_count and
            flagged_non_mines == 0 and
            self.flagged_count == self.mine_count
        )
        return all_safe_cells_revealed or all_mines_flagged
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return GameState(
            game_id=self.game_id,
            width=self.width,
            height=self.height,
            mine_count=self.mine_count,
            revealed_count=self.revealed_count,
            flagged_count=self.flagged_count,
            status=self.status,
            board=self.board,
            created_at=self.created_at,
            last_updated=self.last_updated
        )
    
    def get_public_board(self) -> List[List[Cell]]:
        """
        Get the board state for public display (hides mine locations).
        
        Returns:
            Board with mine locations hidden for non-revealed cells
        """
        public_board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.board[y][x]
                public_cell = Cell(
                    x=cell.x,
                    y=cell.y,
                    state=cell.state,
                    is_mine=cell.is_mine if cell.state == CellState.REVEALED else False,
                    neighbor_mines=cell.neighbor_mines if cell.state == CellState.REVEALED else 0,
                    is_revealed=cell.is_revealed
                )
                row.append(public_cell)
            public_board.append(row)
        return public_board


class GameManager:
    """Manages multiple game instances."""
    
    def __init__(self):
        self.games: dict[str, MinesweeperGame] = {}
    
    def create_game(self, difficulty: Difficulty, width: int = None, height: int = None, mine_count: int = None) -> str:
        """
        Create a new game.
        """
        # Use default config for predefined difficulties
        if difficulty != Difficulty.CUSTOM:
            config = DIFFICULTY_CONFIGS[difficulty]
            width = int(config["width"])
            height = int(config["height"])
            mine_count = int(config["mine_count"])
        else:
            width = int(width)
            height = int(height)
            mine_count = int(mine_count)
        # Validate mine count
        max_mines = width * height - 1  # Leave at least one safe cell
        if mine_count > max_mines:
            mine_count = max_mines
        game = MinesweeperGame(width, height, mine_count)
        self.games[game.game_id] = game
        return game.game_id
    
    def get_game(self, game_id: str) -> MinesweeperGame:
        """Get a game by ID."""
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game."""
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False
    
    def list_games(self) -> List[MinesweeperGame]:
        """List all active games."""
        return list(self.games.values())
    
    def cleanup_old_games(self, max_age_hours: int = 24):
        """Clean up old completed games."""
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        games_to_remove = []
        
        for game_id, game in self.games.items():
            if (game.status in [GameStatus.WON, GameStatus.LOST] and 
                game.last_updated.timestamp() < cutoff_time):
                games_to_remove.append(game_id)
        
        for game_id in games_to_remove:
            del self.games[game_id]


# Global game manager instance
game_manager = GameManager() 