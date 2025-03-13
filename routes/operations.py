from typing import Optional
from loguru import logger
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends
from pydantic import BaseModel


from models import model, game, player
from schemas import game_schema

import dependencies.dependencies as deps

router = APIRouter()

@router.get("/new_game")
def new_game(
    model: model.Model = Depends(deps.model_dependency),
    ):
    game = model.create_new_game()
    return RedirectResponse(url=f"/game/{game.id}")


@router.get("/game/{game_id}/state")
async def get_game_state(
    player: player.Player = Depends(deps.player_dependency),
    game: game.Game = Depends(deps.game_dependency),
    ) -> game_schema.GameSchema:
    game.update()
    return game_schema.GameSchema(game=game, player=player)


@router.post("/game/{game_id}/join_round")
async def join_round(
    player: player.Player = Depends(deps.player_dependency),
    ):
    player.playing = True

@router.post("/game/{game_id}/spectate_round")
async def spectate_round(
    player: player.Player = Depends(deps.player_dependency),
    ):
    player.playing = False


class UpdatePlayerNameSchema(BaseModel):
    name: str

@router.post("/game/{game_id}/update_player_name")
async def update_player_name(
    payload : UpdatePlayerNameSchema,
    player: player.Player = Depends(deps.player_dependency),
    ):
    player.name = payload.name