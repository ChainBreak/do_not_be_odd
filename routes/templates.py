from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import models


import dependencies.dependencies as deps
templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    response: Response,
    user: str = Depends(deps.get_user),
):
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
        },
        response=response,
    )

@router.get("/play/{game_id}", response_class=HTMLResponse)
async def play(
    request: Request,
    response: Response,
    game_id: str,
    user: str = Depends(deps.get_user),
    model: models.Model = Depends(deps.get_model),
    ):

    game = model.games[game_id]

    return templates.TemplateResponse(
        name="play.html", 
        context={
            "request": request,
            "game_id": game.id,
        },
        response=response,
        )