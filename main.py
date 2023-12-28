from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class = HTMLResponse)
def home():
    return """
    <h1>Welcome</h1>
    <a href='http://127.0.0.1:8000/docs'>http://127.0.0.1:8000/docs</a><br>
    <a href='http://127.0.0.1:8000/redoc'>http://127.0.0.1:8000/redoc</a>

"""

