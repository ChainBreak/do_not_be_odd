

import fastapi
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
        response: fastapi.Response,
        model: model.Model = fastapi.Depends(get_model),
    ):
    """Dependency that adds a unqiue user_id to the cookie in the response if it does not exist"""

    user_id = request.cookies.get("user_id", None)

    user = model.get_user(user_id)

    response.set_cookie(
        key="user_id", 
        value=user.id,
        )

    return user