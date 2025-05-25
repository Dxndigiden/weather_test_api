from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import locale

from app.services.weather import get_weather


app = FastAPI()
templates = Jinja2Templates(directory='app/templates')
locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/', response_class=HTMLResponse)
async def get_forecast(request: Request, city: str = Form(...)):
    forecast_raw = await get_weather(city)

    if not isinstance(forecast_raw['temperature'], list):
        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'city': city,
                'forecast': [],
                'error': 'Не удалось получить корректный прогноз.'
            }
        )

    forecast = []
    for time_str, temp in zip(forecast_raw['time'], forecast_raw['temperature']):
        dt = datetime.fromisoformat(time_str)
        formatted_time = dt.strftime('%a, %d %B в %H:%M')
        forecast.append({'time': formatted_time, 'temp': temp})

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'city': city,
            'forecast': forecast
        }
    )