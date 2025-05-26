from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud.forecast import get_top_cities
from app.db.session import SessionLocal

templates = Jinja2Templates(directory='app/templates')

router = APIRouter()


@router.get('/top', response_class=HTMLResponse)
def top_cities(request: Request):
    """Страница с топом запрашиваемых городов."""
    db: Session = SessionLocal()
    try:
        top = get_top_cities(db)
        return templates.TemplateResponse(
            'top.html',
            {'request': request, 'top': top}
        )
    finally:
        db.close()
