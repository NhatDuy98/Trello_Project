from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from v1.routes.user_router import router as user_router
from v1.routes.home_router import router as home_router
from v1.routes.work_space_router import router as work_space_router
from v1.routes.board_router import router as board_router
from v1.main_v1 import v1_router


app = FastAPI()
app.include_router(home_router)
app.include_router(user_router)
app.include_router(work_space_router)
app.include_router(v1_router)

@app.get("/", response_class = HTMLResponse)
def home():
    return """
    <h1>Welcome</h1>
    <a href='http://127.0.0.1:8000/docs'>http://127.0.0.1:8000/docs</a><br>
    <a href='http://127.0.0.1:8000/redoc'>http://127.0.0.1:8000/redoc</a>

"""

