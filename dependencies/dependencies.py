

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
