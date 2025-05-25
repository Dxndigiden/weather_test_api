from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import os

app = FastAPI(title="Weather App")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/weather", response_class=HTMLResponse)
async def show_weather(request: Request, city: str = Form(...)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "city": city,
        "result": f"Погода для {city} будет здесь."
    })
