import httpx


async def get_weather(city: str) -> dict:
    """
    Получить прогноз температуры по названию города.

    Используется API Open-Meteo для геокодирования
    и получения прогноза.
    """
    async with httpx.AsyncClient() as client:
        geo = await client.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={
                'name': city,
                'count': 1,
                'language': 'ru',
                'format': 'json'
            }
        )
        geo_data = geo.json()

        if not geo_data.get('results'):
            return {'temperature': [], 'time': []}

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        weather = await client.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': lat,
                'longitude': lon,
                'hourly': 'temperature_2m',
                'forecast_days': 2,
                'timezone': 'auto'
            }
        )

        return weather.json()['hourly']


async def get_city_suggestions(query: str) -> list[str]:
    """
    Получить подсказки городов по запросу.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={
                'name': query,
                'count': 5,
                'language': 'ru',
                'format': 'json'
            }
        )
        data = response.json()
        results = data.get('results', [])
        return [item['name'] for item in results]
