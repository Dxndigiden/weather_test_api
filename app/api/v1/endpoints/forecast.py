from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.schemas.forecast import ForecastCreate
from app.crud.forecast import create_forecast
from app.services.weather import get_weather
from app.db.session import SessionLocal
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

templates = Jinja2Templates(directory='app/templates')
router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Отображает главную страницу с формой запроса"""
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
async def get_forecast(
    request: Request,
    city: str = Form(...),
    day: str = Form('today')
):
    """Обрабатывает запрос погоды и отображает прогноз"""
    db = SessionLocal()
    raw = await get_weather(city)

    if not raw['temperature_2m'] or not raw['time']:
        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'city': city,
                'forecast': [],
                'error': 'Не удалось получить прогноз.'
            }
        )

    now = datetime.now()
    if day == 'tomorrow':
        start = (now + timedelta(days=1)).date()
    else:
        start = now.date()

    forecast = []
    for t, temp in zip(raw['time'], raw['temperature_2m']):
        dt = datetime.fromisoformat(t)
        if dt.date() == start:
            time_str = dt.strftime('%H:%M')
            forecast.append({'time': time_str, 'temp': temp})

    create_forecast(db=db, obj_in=ForecastCreate(city=city, day=day))

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'city': city,
            'forecast': forecast,
            'selected_day': day
        }
    )
