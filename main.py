import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi import Request, Response
import routes.templates
import routes.websockets
import routes.operations
import dependencies.dependencies as deps
from loguru import logger

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(routes.templates.router)
app.include_router(routes.websockets.router)
app.include_router(routes.operations.router)

@app.middleware("http")
async def add_user_id_cookie(request: Request, call_next):

    model = deps.get_model()

    user_id = request.cookies.get("user_id", None)
    
    if user_id not in model.users:
        user = model.add_new_user()
        user_id = user.id

    request.state.user_id = user_id

    # Get the response
    response: Response = await call_next(request)

    # Add our user_id cookie to the response
    response.set_cookie("user_id", user_id)

    return response
