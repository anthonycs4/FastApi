from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def inicio():
    return """
    <h1>Bienvenido</h1>
    """
