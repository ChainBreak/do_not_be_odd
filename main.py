import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi import Request, Response
import routes.templates
import routes.websockets
import routes.operations
import dependencies.dependencies as deps
from loguru import logger

app = fastapi.FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(routes.templates.router)
app.include_router(routes.websockets.router)
app.include_router(routes.operations.router)

@app.middleware("http")
async def add_session_id_cookie(request: Request, call_next):

    model = deps.model_dependency()

    session_id = request.cookies.get("session_id", None)
    
    if session_id not in model.sessions:
        session_id = model.add_new_session()


    request.state.session_id = session_id

    # Get the response
    response: Response = await call_next(request)

    # Add our session_id cookie to the response
    response.set_cookie("session_id", session_id)

    return response
