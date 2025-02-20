import multiprocessing
import threading
from typing import Optional
import fastapi
from loguru import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends, Response
import dependencies.dependencies as deps
from model import model
from fastapi import WebSocket

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(
    request:Request,
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

@app.get("/new_game")
def new_game(
    model = Depends(deps.get_model),
    user: str = Depends(deps.get_user),
    ):
    
    game = model.create_new_game()

    return RedirectResponse(url=f"/play/{game.id}")

@app.get("/play/{game_id}", response_class=HTMLResponse)
async def play(
    request: Request,
    response: Response,
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
        },
        response=response,
        )


@app.websocket("/websocket/{game_id}")
async def websocket_endpoint(
    game_id: str,
    websocket: WebSocket, 
    ):
    logger.info(f"WebSocket connection initiated for game {game_id}")
    await websocket.accept()
    cookies = websocket.cookies
    logger.info(f"Cookies received: {cookies.get('user_id')}")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        logger.error(f"WebSocket connection closed with exception: {e}")
    finally:
        await websocket.close()


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
