#!/usr/bin/env python3
"""
Debug script to test win condition
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.game_logic import MinesweeperGame, GameStatus, CellState

def debug_win_condition():
    """Debug the win condition logic"""
    print("🔍 Debugging win condition...")
    
    # Create a small game for testing
    game = MinesweeperGame(width=3, height=3, mine_count=2)
    
    # Manually place mines at specific positions for testing
    game.board[0][0].is_mine = True
    game.board[0][1].is_mine = True
    game.mines_placed = True
    game._calculate_neighbor_mines()
    game.status = GameStatus.PLAYING
    
    print(f"Game state: {game.status}")
    print(f"Mine count: {game.mine_count}")
    print(f"Flagged count: {game.flagged_count}")
    print(f"Revealed count: {game.revealed_count}")
    
    # Flag the first mine
    print("\n🎯 Flagging first mine (0,0)...")
    result = game.flag_cell(0, 0)
    print(f"Flag result: {result}")
    print(f"Flagged count: {game.flagged_count}")
    print(f"Game status: {game.status}")
    
    # Check win condition manually
    print("\n🔍 Checking win condition manually...")
    total_cells = game.width * game.height
    all_safe_cells_revealed = game.revealed_count == (total_cells - game.mine_count)
    all_mines_flagged = game.flagged_count == game.mine_count
    
    print(f"Total cells: {total_cells}")
    print(f"All safe cells revealed: {all_safe_cells_revealed}")
    print(f"All mines flagged: {all_mines_flagged}")
    
    # Check flagged mines
    flagged_mines_count = 0
    for y in range(game.height):
        for x in range(game.width):
            cell = game.board[y][x]
            if cell.state == CellState.FLAGGED and cell.is_mine:
                flagged_mines_count += 1
                print(f"Found flagged mine at ({x}, {y})")
    
    print(f"Flagged mines count: {flagged_mines_count}")
    all_mines_flagged = flagged_mines_count == game.mine_count
    print(f"All mines correctly flagged: {all_mines_flagged}")
    
    # Flag the second mine
    print("\n🎯 Flagging second mine (0,1)...")
    result = game.flag_cell(0, 1)
    print(f"Flag result: {result}")
    print(f"Flagged count: {game.flagged_count}")
    print(f"Game status: {game.status}")
    
    # Check win condition again
    print("\n🔍 Checking win condition after second flag...")
    flagged_mines_count = 0
    for y in range(game.height):
        for x in range(game.width):
            cell = game.board[y][x]
            if cell.state == CellState.FLAGGED and cell.is_mine:
                flagged_mines_count += 1
                print(f"Found flagged mine at ({x}, {y})")
    
    print(f"Flagged mines count: {flagged_mines_count}")
    all_mines_flagged = flagged_mines_count == game.mine_count
    print(f"All mines correctly flagged: {all_mines_flagged}")
    
    # Call the actual win condition check
    print("\n🔍 Calling _check_win_condition()...")
    win_result = game._check_win_condition()
    print(f"Win condition result: {win_result}")
    print(f"Final game status: {game.status}")

if __name__ == "__main__":
    debug_win_condition() 