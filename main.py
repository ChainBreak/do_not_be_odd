import multiprocessing
import threading
from typing import Optional
import fastapi
from loguru import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends
import dependencies.dependencies as deps
from model import model

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(
    request:Request,
    ):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/new_game")
def new_game(
    model = Depends(deps.get_model),
    ):
    
    game = model.create_new_game()

    return RedirectResponse(url=f"/play/{game.id}")

@app.get("/play/{game_id}", response_class=HTMLResponse)
async def play(
    request: Request,
    game_id: str,
    user: str = Depends(deps.get_user),
    model: model.Model = Depends(deps.get_model),
    ):

    logger.info(f"{model=}")
    game = model.active_games[game_id]
    logger.info(f"Process name: {multiprocessing.current_process().name}")
    logger.info(f"Thread name: {threading.current_thread().name}")

    return templates.TemplateResponse("play.html", {
        "request": request,
        "game_id": game.id,})


@app.get("/update_user")
async def update_user(
    key:str,
    value:str,
    user: str = Depends(deps.get_user),
    ):

    user.__setattr__(key, value)

    return {"message": "User updated", "user": user}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
