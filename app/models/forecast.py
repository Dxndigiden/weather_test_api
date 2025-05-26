from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class Forecast(Base):
    """Модель прогноза погоды"""
    __tablename__ = 'forecasts'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    day = Column(String, default='today')  # today или tomorrow
    created_at = Column(DateTime, default=datetime.utcnow)
