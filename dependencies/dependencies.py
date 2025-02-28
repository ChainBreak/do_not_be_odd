

import fastapi
from fastapi.responses import RedirectResponse
from loguru import logger
from models import model
import functools


@functools.lru_cache()
def model_dependency() -> model.Model:
    """Dependency that returns a new model instance"""
    logger.info("Creating new model")
    return model.Model()

def session_dependency(
        request: fastapi.Request, 
        model: model.Model = fastapi.Depends(model_dependency),
    ):
    """Dependency that returns the user from the cookie"""
    state_session_id = request.state.session_id 
    
    return model.sessions[state_session_id]

def game_dependency(
        game_id: str,
        model: model.Model = fastapi.Depends(model_dependency),
    ):
    """Dependency that returns the game from the game_id"""
    return model.games.get(game_id,None)

def player_dependency(
        session: model.Session = fastapi.Depends(session_dependency),
        game: model.Game = fastapi.Depends(game_dependency),
    ):
    """Dependency that returns the player from the player_id"""
    if game is None:
        return None
    
    if session.id not in game.players:
        game.add_new_player(session)
    return game.players[session.id]