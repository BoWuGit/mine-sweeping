"""
Unit tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.models import Difficulty

client = TestClient(app)


class TestGameAPI:
    """Test cases for game API endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_api_info_endpoint(self):
        """Test the API info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Minesweeper Game API"
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/game/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "active_games" in data
    
    def test_create_new_game_easy(self):
        """Test creating a new game with easy difficulty."""
        response = client.post("/game/new", json={
            "difficulty": "easy"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"] is not None
        assert data["game_state"]["width"] == 10
        assert data["game_state"]["height"] == 10
        assert data["game_state"]["mine_count"] == 10
        assert data["game_state"]["status"] == "playing"
    
    def test_create_new_game_medium(self):
        """Test creating a new game with medium difficulty."""
        response = client.post("/game/new", json={
            "difficulty": "medium"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["width"] == 16
        assert data["game_state"]["height"] == 16
        assert data["game_state"]["mine_count"] == 40
    
    def test_create_new_game_hard(self):
        """Test creating a new game with hard difficulty."""
        response = client.post("/game/new", json={
            "difficulty": "hard"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["width"] == 16
        assert data["game_state"]["height"] == 30
        assert data["game_state"]["mine_count"] == 99
    
    def test_create_new_game_custom(self):
        """Test creating a new game with custom parameters."""
        response = client.post("/game/new", json={
            "difficulty": "custom",
            "width": 8,
            "height": 8,
            "mine_count": 10
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["width"] == 8
        assert data["game_state"]["height"] == 8
        assert data["game_state"]["mine_count"] == 10
    
    def test_create_custom_game_missing_mine_count(self):
        """Test creating custom game without mine_count."""
        response = client.post("/game/new", json={
            "difficulty": "custom",
            "width": 8,
            "height": 8
        })
        assert response.status_code == 400
    
    def test_create_custom_game_invalid_mine_count(self):
        """Test creating custom game with too many mines."""
        response = client.post("/game/new", json={
            "difficulty": "custom",
            "width": 5,
            "height": 5,
            "mine_count": 25  # More than possible (max is 24)
        })
        assert response.status_code == 400
    
    def test_get_game_state(self):
        """Test getting game state."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Get game state
        response = client.get(f"/game/{game_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["game_id"] == game_id
    
    def test_get_nonexistent_game(self):
        """Test getting a game that doesn't exist."""
        response = client.get("/game/nonexistent")
        assert response.status_code == 404
    
    def test_reveal_cell(self):
        """Test revealing a cell."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Reveal a cell
        response = client.post(f"/game/{game_id}/reveal", json={"x": 0, "y": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["revealed_count"] > 0
    
    def test_reveal_cell_invalid_coordinates(self):
        """Test revealing a cell with invalid coordinates."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Try invalid coordinates
        response = client.post(f"/game/{game_id}/reveal", json={"x": -1, "y": 0})
        assert response.status_code == 422
    
    def test_reveal_cell_nonexistent_game(self):
        """Test revealing a cell in a nonexistent game."""
        response = client.post("/game/nonexistent/reveal", json={"x": 0, "y": 0})
        assert response.status_code == 404
    
    def test_flag_cell(self):
        """Test flagging a cell."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Flag a cell
        response = client.post(f"/game/{game_id}/flag", json={"x": 0, "y": 0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["flagged_count"] == 1
    
    def test_flag_cell_invalid_coordinates(self):
        """Test flagging a cell with invalid coordinates."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Try invalid coordinates
        response = client.post(f"/game/{game_id}/flag", json={"x": 100, "y": 0})
        assert response.status_code == 422
    
    def test_flag_cell_nonexistent_game(self):
        """Test flagging a cell in a nonexistent game."""
        response = client.post("/game/nonexistent/flag", json={"x": 0, "y": 0})
        assert response.status_code == 404
    
    def test_list_games(self):
        """Test listing all games."""
        # Create a few games
        client.post("/game/new", json={"difficulty": "easy"})
        client.post("/game/new", json={"difficulty": "medium"})
        
        response = client.get("/game/")
        assert response.status_code == 200
        data = response.json()
        assert "games" in data
        assert "total" in data
        assert data["total"] >= 2
    
    def test_delete_game(self):
        """Test deleting a game."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Delete the game
        response = client.delete(f"/game/{game_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game deleted successfully"
        
        # Try to get the deleted game
        get_response = client.get(f"/game/{game_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_game(self):
        """Test deleting a game that doesn't exist."""
        response = client.delete("/game/nonexistent")
        assert response.status_code == 404
    
    def test_restart_game(self):
        """Test restarting a game."""
        # Create a game first
        create_response = client.post("/game/new", json={"difficulty": "easy"})
        game_id = create_response.json()["game_state"]["game_id"]
        
        # Restart the game
        response = client.post(f"/game/{game_id}/restart")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["game_state"]["game_id"] != game_id  # New game ID
        assert data["game_state"]["status"] == "playing"
        assert data["game_state"]["revealed_count"] == 0
    
    def test_restart_nonexistent_game(self):
        """Test restarting a game that doesn't exist."""
        response = client.post("/game/nonexistent/restart")
        assert response.status_code == 404
    
    def test_game_flow_win(self):
        """Test a complete game flow that results in a win."""
        # Create a small game with few mines
        response = client.post("/game/new", json={
            "difficulty": "custom",
            "width": 5,
            "height": 5,
            "mine_count": 1
        })
        game_id = response.json()["game_state"]["game_id"]
        
        # Reveal cells until we find the mine or win
        for y in range(5):
            for x in range(5):
                reveal_response = client.post(f"/game/{game_id}/reveal", json={"x": x, "y": y})
                data = reveal_response.json()
                
                if data["game_state"]["status"] == "won":
                    assert "Congratulations" in data["message"]
                    return
                elif data["game_state"]["status"] == "lost":
                    assert "Game Over" in data["message"]
                    return
        
        # If we get here, the game should be won
        final_response = client.get(f"/game/{game_id}")
        final_data = final_response.json()
        assert final_data["game_state"]["status"] in ["won"]


if __name__ == "__main__":
    pytest.main([__file__]) 