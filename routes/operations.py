from typing import Optional
from loguru import logger
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends, Response

from models import model
from fastapi import WebSocket

import dependencies.dependencies as deps

router = APIRouter()

@router.get("/new_game")
def new_game(
    model: model.Model = Depends(deps.get_model),
    ):
    
    game = model.create_new_game()

    return RedirectResponse(url=f"/play/{game.id}")

@router.get("/update_user")
async def update_user(
    key:str,
    value:str,
    user: str = Depends(deps.get_user),
    ):

    user.__setattr__(key, value)

    return {"message": "User updated", "user": user}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}