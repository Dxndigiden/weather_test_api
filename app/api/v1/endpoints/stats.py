from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud.forecast import get_top_cities
from app.db.session import SessionLocal

templates = Jinja2Templates(directory='app/templates')

router = APIRouter()


@router.get('/top', response_class=HTMLResponse)
def top_cities_html(request: Request):
    """HTML-страница с топом самых популярных городов."""
    db: Session = SessionLocal()
    try:
        top = get_top_cities(db)
        return templates.TemplateResponse(
            'top.html',
            {'request': request, 'top': top}
        )
    finally:
        db.close()


@router.get('/api/v1/top')
def top_cities_api():
    """API: возвращает топ городов в формате JSON."""
    db: Session = SessionLocal()
    try:
        top = get_top_cities(db)
        return [{'city': city, 'count': count} for city, count in top]
    finally:
        db.close()
