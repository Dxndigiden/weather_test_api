from fastapi import APIRouter

from app.api.v1.endpoints import forecast, stats, autocomplete

router = APIRouter()
router.include_router(forecast.router, prefix='', tags=['Forecast'])
router.include_router(stats.router, prefix='', tags=['Stats'])
router.include_router(
    autocomplete.router,
    prefix='/api/v1',
    tags=['Autocomplete']
)
