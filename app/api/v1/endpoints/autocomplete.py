from fastapi import APIRouter, Query
from typing import List

from app.services.weather import get_city_suggestions

router = APIRouter()


@router.get('/autocomplete', response_model=List[str])
async def autocomplete_city(q: str = Query(..., min_length=2)):
    """
    Получить подсказки для ввода города.
    """
    suggestions = await get_city_suggestions(q)
    return suggestions
