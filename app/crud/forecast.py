from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.forecast import Forecast
from app.schemas.forecast import ForecastCreate


def create_forecast(db: Session, obj_in: ForecastCreate) -> Forecast:
    """Сохраняет прогноз в базу"""
    db_obj = Forecast(city=obj_in.city, day=obj_in.day)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_top_cities(db: Session, limit: int = 5) -> list[tuple[str, int]]:
    """Получить топ городов по количеству запросов."""
    return (
        db.query(Forecast.city, func.count(Forecast.id).label('count'))
        .group_by(Forecast.city)
        .order_by(func.count(Forecast.id).desc())
        .limit(limit)
        .all()
    )
