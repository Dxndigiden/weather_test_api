import httpx


async def get_weather(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        geo = await client.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={'name': city, 'count': 1, 'language': 'ru', 'format': 'json'}
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
                'forecast_days': 1,
                'timezone': 'auto'
            }
        )

        weather_data = weather.json()
        return {
            'temperature': weather_data['hourly']['temperature_2m'],
            'time': weather_data['hourly']['time']
        }
