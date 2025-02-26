

import fastapi
from fastapi.responses import RedirectResponse
from loguru import logger
from models import model
import functools


@functools.lru_cache()
def get_model() -> model.Model:
    """Dependency that returns a new model instance"""
    logger.info("Creating new model")
    return model.Model()

def get_user(
        request: fastapi.Request, 
        model: model.Model = fastapi.Depends(get_model),
    ):
    """Dependency that returns the user from the cookie"""
    cookie_user_id = request.cookies.get("user_id",None)
    state_user_id = request.state.user_id 
    
    logger.debug(f"Cookie user id: {cookie_user_id}. State user id: {state_user_id}")

    return model.users[state_user_id]
