"""
Main FastAPI application for the Minesweeper game.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import router as game_router

# Create FastAPI app
app = FastAPI(
    title="Minesweeper Game API",
    description="A complete Minesweeper game API with support for multiple games",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game routes
app.include_router(game_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return JSONResponse(
        content={
            "message": "Welcome to Minesweeper Game API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/game/health"
        }
    )


@app.get("/info")
async def api_info():
    """Get detailed API information."""
    return JSONResponse(
        content={
            "name": "Minesweeper Game API",
            "version": "1.0.0",
            "description": "A complete Minesweeper game implementation with FastAPI",
            "features": [
                "Multiple game support",
                "Configurable difficulty levels",
                "Real-time game state",
                "Complete REST API",
                "Interactive documentation"
            ],
            "endpoints": {
                "docs": "/docs",
                "health": "/game/health",
                "new_game": "POST /game/new",
                "get_game": "GET /game/{game_id}",
                "reveal_cell": "POST /game/{game_id}/reveal",
                "flag_cell": "POST /game/{game_id}/flag",
                "list_games": "GET /game/",
                "delete_game": "DELETE /game/{game_id}",
                "restart_game": "POST /game/{game_id}/restart"
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 