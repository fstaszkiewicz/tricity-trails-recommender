# src/models/weather_data.py
from datetime import datetime

class WeatherData:
    """
    Klasa do przechowywania danych pogodowych dla konkretnej godziny.
    """
    def __init__(self, timestamp: datetime, temperature: float,
                 precipitation_probability: int, precipitation_amount: float,
                 sunshine_duration: float, cloud_cover: int):
        """
        Inicjalizuje obiekt WeatherData.

        Argumenty:
            timestamp (datetime): Znacznik czasu dla danych pogodowych (obiekt datetime).
            temperature (float): Temperatura w stopniach Celsjusza (°C).
            precipitation_probability (int): Prawdopodobieństwo opadów w procentach (%).
            precipitation_amount (float): Suma opadów w milimetrach (mm).
            sunshine_duration (float): Czas nasłonecznienia w sekundach w ciągu godziny.
            cloud_cover (int): Zachmurzenie w procentach (%).
        """
        self.timestamp: datetime = timestamp
        self.temperature: float = temperature
        self.precipitation_probability: int = precipitation_probability
        self.precipitation_amount: float = precipitation_amount
        self.sunshine_duration: float = sunshine_duration  # w sekundach
        self.cloud_cover: int = cloud_cover

    def __str__(self) -> str:
        """
        Zwraca reprezentację stringową obiektu WeatherData.
        """
        return (f"Czas: {self.timestamp.strftime('%Y-%m-%d %H:%M')}, "
                f"Temp: {self.temperature}°C, "
                f"Prawd. opadów: {self.precipitation_probability}%, "
                f"Opad: {self.precipitation_amount}mm, "
                f"Nasłonecznienie: {self.sunshine_duration}s, "
                f"Zachmurzenie: {self.cloud_cover}%")