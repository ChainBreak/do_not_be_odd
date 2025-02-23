from typing import Optional
import fastapi
from loguru import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, Response

from model import model
from fastapi import WebSocket

router = APIRouter()

@router.websocket("/websocket/{game_id}")
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