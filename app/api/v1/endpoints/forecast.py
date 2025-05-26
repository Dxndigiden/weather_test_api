from datetime import datetime, timedelta
from urllib.parse import quote, unquote

import locale
from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas.forecast import ForecastCreate
from app.crud.forecast import create_forecast
from app.services.weather import get_weather
from app.db.session import SessionLocal

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
def show_form(
    request: Request,
    last_city: str = Cookie(default='')
) -> HTMLResponse:
    """Показывает форму с городом из cookie, декодируя его."""
    city = unquote(last_city) if last_city else ''
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'city': city,
            'selected_day': 'today',
            'forecast': None,
            'error': None
        }
    )


@router.post('/', response_class=HTMLResponse)
async def get_forecast(
    request: Request,
    city: str = Form(...),
    day: str = Form('today')
) -> HTMLResponse:
    """Получает прогноз по городу и дню,
    сохраняет запрос, показывает результат."""
    db = SessionLocal()
    raw = await get_weather(city)

    if not raw.get('temperature_2m') or not raw.get('time'):
        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'city': city,
                'forecast': [],
                'error': 'Не удалось получить прогноз.',
                'selected_day': day
            }
        )

    now = datetime.now()
    start_date = (
        now + timedelta(days=1)
    ).date() if day == 'tomorrow' else now.date()

    forecast = []
    for t, temp in zip(raw['time'], raw['temperature_2m']):
        dt = datetime.fromisoformat(t)
        if dt.date() == start_date:
            forecast.append({
                'time': dt.strftime('%H:%M'),
                'temp': temp
            })

    create_forecast(db=db, obj_in=ForecastCreate(city=city, day=day))

    response = templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'city': city,
            'forecast': forecast,
            'selected_day': day
        }
    )
    encoded_city = quote(city, safe='')
    response.set_cookie(
        key='last_city',
        value=encoded_city,
        max_age=60 * 60 * 24 * 30
    )
    return response
