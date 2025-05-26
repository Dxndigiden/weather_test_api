from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.endpoints import forecast, stats
from app.db.base import Base
from app.db.session import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

templates = Jinja2Templates(directory='app/templates')

app.include_router(forecast.router, prefix='', tags=['Forecast'])
app.include_router(stats.router, prefix='/stats', tags=['Stats'])
