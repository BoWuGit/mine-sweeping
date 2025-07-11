"""
API routes for the Minesweeper game.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .models import (
    NewGameRequest, RevealRequest, FlagRequest, GameResponse, 
    GameListResponse, Difficulty, DIFFICULTY_CONFIGS
)
from .game_logic import game_manager

router = APIRouter(prefix="/game", tags=["game"])


# Health check endpoint - must be before parameter routes
@router.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "active_games": len(game_manager.list_games())
        }
    )


@router.post("/new", response_model=GameResponse)
async def create_new_game(request: NewGameRequest):
    """
    Create a new Minesweeper game.
    """
    try:
        if request.difficulty == Difficulty.CUSTOM:
            if request.mine_count is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "message": "mine_count is required for custom difficulty",
                        "error": "mine_count is required for custom difficulty",
                        "game_state": None
                    }
                )
            max_mines = int(request.width) * int(request.height) - 1
            if int(request.mine_count) > max_mines:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "message": f"mine_count cannot exceed {max_mines} for {request.width}x{request.height} board",
                        "error": f"mine_count cannot exceed {max_mines} for {request.width}x{request.height} board",
                        "game_state": None
                    }
                )
        else:
            # 兼容字符串和Enum类型
            diff = request.difficulty
            if isinstance(diff, str):
                diff = Difficulty(diff)
            config = DIFFICULTY_CONFIGS[diff]
            request.width = config["width"]
            request.height = config["height"]
            request.mine_count = config["mine_count"]
        game_id = game_manager.create_game(
            difficulty=request.difficulty,
            width=request.width,
            height=request.height,
            mine_count=request.mine_count
        )
        game = game_manager.get_game(game_id)
        game_state = game.get_game_state()
        return GameResponse(
            success=True,
            message="New game created successfully",
            game_state=game_state
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Failed to create new game",
                "error": str(e),
                "game_state": None
            }
        )


@router.get("/{game_id}", response_model=GameResponse)
async def get_game_state(game_id: str) -> GameResponse:
    """
    Get the current state of a game.
    
    Args:
        game_id: Unique game identifier
        
    Returns:
        Game response with current state
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    game_state = game.get_game_state()
    return GameResponse(
        success=True,
        message="Game state retrieved successfully",
        game_state=game_state
    )


@router.post("/{game_id}/reveal", response_model=GameResponse)
async def reveal_cell(game_id: str, request: RevealRequest) -> GameResponse:
    """
    Reveal a cell in the game.
    
    Args:
        game_id: Unique game identifier
        request: Cell coordinates
        
    Returns:
        Game response with updated state
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Validate coordinates
    if not (0 <= request.x < game.width and 0 <= request.y < game.height):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Coordinates out of bounds"
        )
    
    # Reveal the cell
    game.reveal_cell(request.x, request.y)
    game_state = game.get_game_state()

    # Check for win/loss after reveal
    if game.status.value == "lost":
        return GameResponse(
            success=True,
            message="Game Over! You hit a mine!",
            game_state=game_state
        )
    elif game.status.value == "won":
        return GameResponse(
            success=True,
            message="Congratulations! You Win!",
            game_state=game_state
        )

    return GameResponse(
        success=True,
        message="Cell revealed successfully",
        game_state=game_state
    )


@router.post("/{game_id}/flag", response_model=GameResponse)
async def flag_cell(game_id: str, request: FlagRequest) -> GameResponse:
    """
    Toggle flag on a cell.
    
    Args:
        game_id: Unique game identifier
        request: Cell coordinates
        
    Returns:
        Game response with updated state
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Validate coordinates
    if not (0 <= request.x < game.width and 0 <= request.y < game.height):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Coordinates out of bounds"
        )
    
    # Toggle flag
    success = game.flag_cell(request.x, request.y)
    if not success:
        return GameResponse(
            success=False,
            message="Cannot flag this cell",
            error="Cell is already revealed or game is not active"
        )
    
    game_state = game.get_game_state()
    
    # Check for win/loss after flagging
    if game.status.value == "won":
        return GameResponse(
            success=True,
            message="Congratulations! You Win!",
            game_state=game_state
        )
    
    return GameResponse(
        success=True,
        message="Flag toggled successfully",
        game_state=game_state
    )


@router.get("/", response_model=GameListResponse)
async def list_games() -> GameListResponse:
    """
    List all active games.
    
    Returns:
        List of all active games
    """
    games = game_manager.list_games()
    game_states = [game.get_game_state() for game in games]
    
    return GameListResponse(
        games=game_states,
        total=len(game_states)
    )


@router.delete("/{game_id}")
async def delete_game(game_id: str) -> JSONResponse:
    """
    Delete a game.
    
    Args:
        game_id: Unique game identifier
        
    Returns:
        Success response
    """
    success = game_manager.delete_game(game_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Game deleted successfully"}
    )


@router.post("/{game_id}/restart")
async def restart_game(game_id: str) -> GameResponse:
    """
    Restart a game with the same configuration.
    
    Args:
        game_id: Unique game identifier
        
    Returns:
        Game response with new game state
    """
    old_game = game_manager.get_game(game_id)
    if not old_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Delete old game
    game_manager.delete_game(game_id)
    
    # Create new game with same configuration
    new_game_id = game_manager.create_game(
        difficulty=Difficulty.CUSTOM,  # Use custom to specify exact dimensions
        width=old_game.width,
        height=old_game.height,
        mine_count=old_game.mine_count
    )
    
    new_game = game_manager.get_game(new_game_id)
    game_state = new_game.get_game_state()
    
    return GameResponse(
        success=True,
        message="Game restarted successfully",
        game_state=game_state
    ) 