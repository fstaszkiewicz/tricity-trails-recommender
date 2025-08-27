import datetime
from typing import List, Dict, Any
from collections import defaultdict

from src.models.route import Route
from src.models.user_preference import UserPreference
from src.models.weather_data import WeatherData
from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.utils.constants import NIGHT_HOURS, CLOUD_COVER_PREFERENCES, COMFORT_COLOR_THRESHOLDS, TRICITY_COORDS, FORECAST_DAYS

class RouteRecommender:
    def __init__(self, route_manager: RouteDataManager, weather_manager: WeatherDataManager):
        """
        Inicjalizuje recommender z dostępem do managerów danych.
        """
        self._route_manager = route_manager
        self._weather_manager = weather_manager
        print("RouteRecommender initialized.")

    def filter_routes(self, preferences: UserPreference) -> List[Route]:
        """
        Filtruje trasy na podstawie podstawowych preferencji użytkownika, ignorując duplikaty.
        """
        print("\n--- Rozpoczęcie filtrowania tras ---")
        print(f"Preferencje użytkownika: {preferences}")

        all_routes = self._route_manager.routes
        filtered_routes = []
        seen_names = set()

        for route in all_routes:
            if route.name in seen_names:
                continue

            if self._route_manager.check_route_match_preferences(route, preferences):
                filtered_routes.append(route)
                seen_names.add(route.name)

        print(f"Znaleziono {len(filtered_routes)} unikalnych tras po filtracji.")
        return filtered_routes

    def _calculate_hourly_comfort(self, weather_hour: WeatherData, preferences: UserPreference) -> float:
        """
        Oblicza indeks komfortu (0-100) dla pojedynczej godziny na podstawie preferencji.
        """

        """
        Jeśli temperatura mieści się w widełkach preferowanych przez użytkownika 
        (np. między 15°C a 25°C), wynik pozostaje 100.
        Jeśli temperatura wykracza poza ten zakres, wynik jest karany. 
        Obliczana jest różnica (temp_diff) między faktyczną temperaturą a najbliższą granicą widełek.
        Za każdy 1 stopień Celsjusza tej różnicy, od wyniku odejmowane jest 10 punktów.
        Funkcja max() zapewnia, że wynik nie spadnie poniżej zera.
        """
        temp_score = 100.0
        if not (preferences.min_temp <= weather_hour.temperature <= preferences.max_temp):
            temp_diff = min(abs(weather_hour.temperature - preferences.min_temp),
                            abs(weather_hour.temperature - preferences.max_temp))
            temp_score = max(0, 100 - temp_diff * 10)

        """
        Jeśli użytkownik zaznaczył, że nie akceptuje opadów, 
        a prognoza przewiduje jakiekolwiek opady (precipitation_amount > 0),
        wynik jest natychmiast zerowany (precip_score = 0.0).
        Jeśli użytkownik akceptuje opady, ale one występują, wynik jest stopniowo karany. 
        Za każdy 1 mm opadu na godzinę, od wyniku odejmowane jest 20 punktów.
        """
        precip_score = 100.0
        if not preferences.allow_precipitation and weather_hour.precipitation_amount > 0:
            precip_score = 0.0
        elif weather_hour.precipitation_amount > 0:
            precip_score = max(0, 100 - weather_hour.precipitation_amount * 20)

        """
        Najpierw z pliku constants.py pobierany jest preferowany przez użytkownika zakres zachmurzenia
        (np. dla "troche_chmur" jest to przedział 30-70%).
        Jeśli faktyczne zachmurzenie wykracza poza ten zakres, wynik jest redukowany do stałej wartości 50.0. 
        Albo warunek jest spełniony (100 pkt), albo nie (50 pkt).
        """
        cloud_score = 100.0
        pref_cloud_range = CLOUD_COVER_PREFERENCES[preferences.preferred_cloud_cover]
        if not (pref_cloud_range[0] <= weather_hour.cloud_cover <= pref_cloud_range[1]):
            cloud_score = 50.0

        final_comfort = (temp_score + precip_score + cloud_score) / 3
        return final_comfort

    def calculate_daily_comfort_for_route(self, route: Route, preferences: UserPreference) -> List[Dict[str, Any]]:
        """
        Oblicza średni dzienny komfort dla danej trasy na najbliższe 14 dni.
        """
        coords = TRICITY_COORDS.get(route.region)
        if not coords:
            coords = TRICITY_COORDS["Trójmiasto"]

        weather_forecast = self._weather_manager.get_weather_for_location(coords['latitude'], coords['longitude'])
        if not weather_forecast:
            return []


        daily_weather = defaultdict(list)
        for hour_data in weather_forecast:
            daily_weather[hour_data.timestamp.date()].append(hour_data)

        daily_comfort_scores = []
        for i in range(FORECAST_DAYS):
            day = datetime.date.today() + datetime.timedelta(days=i)
            hourly_comforts_for_day = []
            if day in daily_weather:
                for weather_hour in daily_weather[day]:
                    if weather_hour.timestamp.hour in NIGHT_HOURS and not preferences.allow_night_walks:
                        continue
                    hourly_comforts_for_day.append(self._calculate_hourly_comfort(weather_hour, preferences))

            avg_comfort = sum(hourly_comforts_for_day) / len(hourly_comforts_for_day) if hourly_comforts_for_day else 0

            color = "#333333" # Ciemnoszary domyślny
            if avg_comfort >= COMFORT_COLOR_THRESHOLDS['green']:
                color = '#2E8B57'
            elif avg_comfort >= COMFORT_COLOR_THRESHOLDS['yellow']:
                color = '#FFD700'
            elif avg_comfort >= COMFORT_COLOR_THRESHOLDS['orange']:
                color = '#FFA500'
            else:
                color = '#DC143C'

            """
            PRZYKŁAD JAK WYGLĄDAJĄ DANE W daily_comfort_score 
            
            Dzień 1: Dzisiaj (24.05.2025) - pogoda idealna
            {
                "date": datetime.date(2025, 5, 24),
                "score": 93,
                "color": "#2E8B57"  # Zielony, bo score (93) >= 80
            }
        
            Dzień 2: (25.05.2025) - pogoda niezła
            {
                "date": datetime.date(2025, 5, 25),
                "score": 71,
                "color": "#FFD700"  # Żółty, bo score (71) >= 65
            }
            """

            daily_comfort_scores.append({
                "date": day,
                "score": round(avg_comfort),
                "color": color
            })
        return daily_comfort_scores