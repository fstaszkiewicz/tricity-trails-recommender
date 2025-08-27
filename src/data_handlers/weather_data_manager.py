import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
from datetime import datetime

from src.models.weather_data import WeatherData
from src.utils.constants import FORECAST_DAYS


class WeatherDataManager:
    """
    Zarządza pobieraniem i przetwarzaniem danych pogodowych z API
    """
    def __init__(self):
        """
        Inicjalizuje klienta API z pamięcią podręczną i mechanizmem ponawiania.
        """
        # Konfiguracja klienta Open-Meteo API z pamięcią podręczną i ponawianiem prób w razie błędów
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self._openmeteo = openmeteo_requests.Client(session=retry_session)
        print("WeatherDataManager initialized.")

    def get_weather_for_location(self, latitude: float, longitude: float) -> list[WeatherData]:
        """
        Pobiera prognozę pogody dla podanej lokalizacji i zwraca listę obiektów WeatherData.

        Args:
            latitude (float): Szerokość geograficzna.
            longitude (float): Długość geograficzna.

        Returns:
            list[WeatherData]: Lista obiektów z danymi pogodowymi dla kolejnych godzin.
                               Zwraca pustą listę w przypadku błędu.
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "sunshine_duration",
                       "cloud_cover"],
            "timezone": "auto",
            "forecast_days": FORECAST_DAYS
        }

        try:
            responses = self._openmeteo.weather_api(url, params=params)
        except Exception as e:
            print(f"Błąd podczas wywołania API Open-Meteo dla ({latitude}, {longitude}): {e}")
            return []

        if not responses:
            print(f"Brak odpowiedzi z API dla ({latitude}, {longitude}).")
            return []

        response = responses[0]

        # Przetwarzanie danych godzinowych
        hourly = response.Hourly()
        if hourly is None:
            print(f"Brak danych godzinowych w odpowiedzi API dla ({latitude}, {longitude}).")
            return []

        """
        Biblioteka `pandas` jest tutaj używana do zorganizowania tych luźnych list w jedną,
        spójną strukturę danych - tabelę zwaną DataFrame. Każdy wiersz w tej tabeli
        reprezentuje jedną godzinę, a kolumny to poszczególne parametry pogodowe.
        To radykalnie upraszcza dalsze przetwarzanie danych.

        Przykładowy wygląd `hourly_dataframe` po wykonaniu tej operacji:

                                 date  temperature_2m  precipitation_probability  precipitation  sunshine_duration  cloud_cover
        0   2025-05-24 14:00:00+00:00            18.5                         10            0.0             3600.0           25
        1   2025-05-24 15:00:00+00:00            19.1                         15            0.0             3200.0           35
        
        Po stworzeniu tej ustrukturyzowanej tabeli, pętla `for` poniżej używająca metody .iterrows()
        może łatwo przejść przez nią wiersz po wierszu, aby dla każdej godziny stworzyć
        jeden obiekt klasy WeatherData i dodać go do finalnej listy z prognozą.
        """

        # Tworzenie DataFrame z danymi pogodowymi
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "precipitation_probability": hourly.Variables(1).ValuesAsNumpy(),
            "precipitation": hourly.Variables(2).ValuesAsNumpy(),
            "sunshine_duration": hourly.Variables(3).ValuesAsNumpy(),
            "cloud_cover": hourly.Variables(4).ValuesAsNumpy()
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)

        weather_forecast: list[WeatherData] = []
        for _, row in hourly_dataframe.iterrows():
            weather_point = WeatherData(
                timestamp=row['date'],
                temperature=round(float(row['temperature_2m']), 1),
                precipitation_probability=int(row['precipitation_probability']),
                precipitation_amount=round(float(row['precipitation']), 2),
                sunshine_duration=float(row['sunshine_duration']),
                cloud_cover=int(row['cloud_cover'])
            )
            weather_forecast.append(weather_point)

        print(
            f"Successfully fetched and processed {len(weather_forecast)} hourly weather points for ({latitude}, {longitude}).")
        return weather_forecast