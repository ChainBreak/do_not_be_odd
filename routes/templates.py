from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import model, game



import dependencies.dependencies as deps
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    session: str = Depends(deps.session_dependency),
    ):
    response = templates.TemplateResponse(
        name="index.html",
        context={"request": request, "session_id":session.id},
    )

    return response

@router.get("/play/{game_id}", response_class=HTMLResponse)
async def play(
    request: Request,
    game_id: str,
    session: str = Depends(deps.session_dependency),
    model: model.Model = Depends(deps.model_dependency),
    game: model.Game = Depends(deps.game_dependency),
    player: game.Player = Depends(deps.player_dependency),
    ):
    

    return templates.TemplateResponse(
        name="play.html", 
        context={
            "request": request,
            "game_id": game.id,
            "session_id":session.id,
            "player": str(player),
        },
        )