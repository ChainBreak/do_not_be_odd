from typing import Optional
import uuid
from collections import defaultdict
import dataclasses
from fastapi import FastAPI, Request, Response, Depends
from loguru import logger

app = FastAPI()




def get_user(request: Request, response: Response):
    """Dependency that adds a unqiue user_id to the cookie in the response if it does not exist"""

    user_id = request.cookies.get("user_id", None)

    user = users[user_id]

    response.set_cookie(key="user_id", value=user.id)

    return user


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/play/{game_id}")
async def game(
    game_id: str,
    user: str = Depends(get_user),
    ):

    logger.debug(users)
    return {"game_id": game_id, "user": user}


@app.get("/update_user")
async def update_user(
    key:str,
    value:str,
    user: str = Depends(get_user),
    ):

    user.__setattr__(key, value)

    return {"message": "User updated", "user": user}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
