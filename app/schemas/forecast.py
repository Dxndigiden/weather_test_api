from pydantic import BaseModel


class ForecastCreate(BaseModel):
    """Схема создания прогноза"""
    city: str
    day: str = 'today'


class ForecastOut(BaseModel):
    """Схема для отображения топа городов."""
    city: str
    count: int
