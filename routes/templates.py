from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import model


import dependencies.dependencies as deps
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    user: str = Depends(deps.get_user),
    ):
    response = templates.TemplateResponse(
        name="index.html",
        context={"request": request, "user_id":user.id},
    )

    return response

@router.get("/play/{game_id}", response_class=HTMLResponse)
async def play(
    request: Request,
    game_id: str,
    user: str = Depends(deps.get_user),
    model: model.Model = Depends(deps.get_model),
    ):
    game = model.games[game_id]

    return templates.TemplateResponse(
        name="play.html", 
        context={
            "request": request,
            "game_id": game.id,
            "user_id":user.id
        },
        )