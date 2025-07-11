"""
Data models for the Minesweeper game API.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class Difficulty(str, Enum):
    """Game difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    CUSTOM = "custom"


class CellState(str, Enum):
    """Cell states in the game."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    EXPLODED = "exploded"


class GameStatus(str, Enum):
    """Game status."""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class NewGameRequest(BaseModel):
    """Request model for creating a new game."""
    difficulty: Difficulty = Field(default=Difficulty.EASY, description="Game difficulty")
    width: int = Field(default=10, ge=5, le=50, description="Board width")
    height: int = Field(default=10, ge=5, le=50, description="Board height")
    mine_count: Optional[int] = Field(default=None, ge=1, description="Number of mines (for custom difficulty)")


class Cell(BaseModel):
    """Represents a single cell in the game board."""
    x: int = Field(description="X coordinate")
    y: int = Field(description="Y coordinate")
    state: CellState = Field(description="Current state of the cell")
    is_mine: bool = Field(description="Whether this cell contains a mine")
    neighbor_mines: int = Field(description="Number of mines in adjacent cells")
    is_revealed: bool = Field(description="Whether this cell has been revealed")


class GameState(BaseModel):
    """Complete game state."""
    game_id: str = Field(description="Unique game identifier")
    width: int = Field(description="Board width")
    height: int = Field(description="Board height")
    mine_count: int = Field(description="Total number of mines")
    revealed_count: int = Field(description="Number of revealed cells")
    flagged_count: int = Field(description="Number of flagged cells")
    status: GameStatus = Field(description="Current game status")
    board: List[List[Cell]] = Field(description="Game board")
    created_at: datetime = Field(description="Game creation timestamp")
    last_updated: datetime = Field(description="Last update timestamp")


class RevealRequest(BaseModel):
    """Request model for revealing a cell."""
    x: int = Field(ge=0, description="X coordinate")
    y: int = Field(ge=0, description="Y coordinate")


class FlagRequest(BaseModel):
    """Request model for flagging a cell."""
    x: int = Field(ge=0, description="X coordinate")
    y: int = Field(ge=0, description="Y coordinate")


class GameResponse(BaseModel):
    """Response model for game operations."""
    success: bool = Field(description="Operation success status")
    message: str = Field(description="Response message")
    game_state: Optional[GameState] = Field(default=None, description="Current game state")
    error: Optional[str] = Field(default=None, description="Error message if operation failed")


class GameListResponse(BaseModel):
    """Response model for listing games."""
    games: List[GameState] = Field(description="List of active games")
    total: int = Field(description="Total number of games")


# Default difficulty configurations
DIFFICULTY_CONFIGS = {
    Difficulty.EASY: {"width": 10, "height": 10, "mine_count": 10},
    Difficulty.MEDIUM: {"width": 16, "height": 16, "mine_count": 40},
    Difficulty.HARD: {"width": 16, "height": 30, "mine_count": 99},
} 