# recommender_app/src/models/user_preference.py

from src.utils.constants import TIME_RANGES, LENGTH_OPTIONS, DIFFICULTY_MULTIPLIERS, MAX_RATING, CLOUD_COVER_PREFERENCES, TRICITY_COORDS


class UserPreference:
    def __init__(self,
                 min_temp: float = -10.0,
                 max_temp: float = 30.0,
                 allow_precipitation: bool = True,
                 preferred_difficulty: str = 'moderate',
                 min_length: float = 1.0,
                 max_length: float = 20.0,
                 min_rating: float = 3.0,  # Przywrócono min_rating
                 allow_night_walks: bool = False,
                 preferred_cloud_cover: str = 'troche_chmur',
                 preferred_city: str = 'Trójmiasto',
                 weight_weather: float = 0.4,  # Dostosowane wagi, aby suma wynosiła 1.0 dla 4 czynników
                 weight_difficulty: float = 0.2,
                 weight_length: float = 0.2,
                 weight_rating: float = 0.2,  # Przywrócono weight_rating
                 preferred_time_range: str = '2-4 godziny'
                 ):

        self.min_temp = min_temp
        self.max_temp = max_temp
        self.allow_precipitation = allow_precipitation
        self.preferred_difficulty = preferred_difficulty
        self.min_length = min_length
        self.max_length = max_length
        self.min_rating = min_rating  # Przywrócono self.min_rating
        self.allow_night_walks = allow_night_walks
        self.preferred_cloud_cover = preferred_cloud_cover
        self.preferred_city = preferred_city
        self.weight_weather = weight_weather
        self.weight_difficulty = weight_difficulty
        self.weight_length = weight_length
        self.weight_rating = weight_rating  # Przywrócono self.weight_rating
        self.preferred_time_range = preferred_time_range

    @property
    def min_temp(self) -> float:
        return self._min_temp # Przykład publicznego dostęp do odczytu

    @min_temp.setter
    def min_temp(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Minimalna temperatura musi być liczbą.")
        self._min_temp = float(value)

    @property
    def max_temp(self) -> float:
        return self._max_temp

    @max_temp.setter
    def max_temp(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Maksymalna temperatura musi być liczbą.")
        self._max_temp = float(value)

    @property
    def allow_precipitation(self) -> bool:
        return self._allow_precipitation

    @allow_precipitation.setter
    def allow_precipitation(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Dopuszczanie opadów musi być wartością logiczną (True/False).")
        self._allow_precipitation = value

    @property
    def preferred_difficulty(self) -> str:
        return self._preferred_difficulty

    @preferred_difficulty.setter
    def preferred_difficulty(self, value: str):
        if value.lower() not in DIFFICULTY_MULTIPLIERS:
            raise ValueError(
                f"Nieznana preferowana trudność: {value}. Dopuszczalne: {list(DIFFICULTY_MULTIPLIERS.keys())}")
        self._preferred_difficulty = value.lower()

    @property
    def min_length(self) -> float:
        return self._min_length

    @min_length.setter
    def min_length(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Minimalna długość musi być nieujemną liczbą.")
        self._min_length = float(value)

    @property
    def max_length(self) -> float:
        return self._max_length

    @max_length.setter
    def max_length(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Maksymalna długość musi być nieujemną liczbą.")
        self._max_length = float(value)

    @property
    def min_rating(self) -> float:  # Przywrócono property min_rating
        return self._min_rating

    @min_rating.setter
    def min_rating(self, value: float):  # Przywrócono setter min_rating
        if not isinstance(value, (int, float)) or not (0 <= value <= MAX_RATING):
            raise ValueError(f"Minimalna ocena musi być liczbą od 0 do {MAX_RATING}.")
        self._min_rating = float(value)

    @property
    def allow_night_walks(self) -> bool:
        return self._allow_night_walks

    @allow_night_walks.setter
    def allow_night_walks(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Zezwolenie na nocne spacery musi być wartością logiczną (True/False).")
        self._allow_night_walks = value

    @property
    def preferred_cloud_cover(self) -> str:
        return self._preferred_cloud_cover

    @preferred_cloud_cover.setter
    def preferred_cloud_cover(self, value: str):
        if value.lower() not in CLOUD_COVER_PREFERENCES:
            raise ValueError(
                f"Nieznana preferencja zachmurzenia: {value}. Dopuszczalne: {list(CLOUD_COVER_PREFERENCES.keys())}")
        self._preferred_cloud_cover = value.lower()

    @property
    def preferred_city(self) -> str:
        return self._preferred_city

    @preferred_city.setter
    def preferred_city(self, value: str):
        from src.utils.constants import TRICITY_COORDS
        valid_cities = list(TRICITY_COORDS.keys()) + ["Trójmiasto"]
        if value.lower() not in [c.lower() for c in valid_cities]:
            raise ValueError(f"Nieznane preferowane miasto: {value}. Dopuszczalne: {valid_cities}")
        self._preferred_city = value

    @property
    def weight_weather(self) -> float:
        return self._weight_weather

    @weight_weather.setter
    def weight_weather(self, value: float):
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            raise ValueError("Waga pogody musi być liczbą od 0 do 1.")
        self._weight_weather = float(value)

    @property
    def weight_difficulty(self) -> float:
        return self._weight_difficulty

    @weight_difficulty.setter  # Poprawiono błąd w nazwie settera
    def weight_difficulty(self, value: float):
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            raise ValueError("Waga trudności musi być liczbą od 0 do 1.")
        self._weight_difficulty = float(value)

    @property
    def weight_length(self) -> float:
        return self._weight_length

    @weight_length.setter  # Poprawiono błąd w nazwie settera
    def weight_length(self, value: float):
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            raise ValueError("Waga długości musi być liczbą od 0 do 1.")
        self._weight_length = float(value)

    @property
    def weight_rating(self) -> float:  # Przywrócono property weight_rating
        return self._weight_rating

    @weight_rating.setter  # Przywrócono setter weight_rating
    def weight_rating(self, value: float):
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            raise ValueError("Waga oceny musi być liczbą od 0 do 1.")
        self._weight_rating = float(value)

    @property
    def preferred_time_range(self) -> str:
        return self._preferred_time_range

    @preferred_time_range.setter
    def preferred_time_range(self, value: str):
        if value not in TIME_RANGES:
            raise ValueError(f"Nieznany preferowany zakres czasu: {value}. Dopuszczalne: {list(TIME_RANGES.keys())}")
        self._preferred_time_range = value

    def get_weights(self) -> dict:
        """Zwraca słownik z wagami dla różnych czynników."""
        return {
            'weather': self._weight_weather,
            'difficulty': self._weight_difficulty,
            'length': self._weight_length,
            'rating': self._weight_rating
        }

    def __repr__(self):
        return (f"UserPreference(MinTemp: {self._min_temp}, MaxTemp: {self._max_temp}, "
                f"AllowPrecip: {self._allow_precipitation}, Difficulty: '{self._preferred_difficulty}', "
                f"MinLength: {self._min_length}, MaxLength: {self._max_length}, "
                f"MinRating: {self._min_rating}, NightWalks: {self._allow_night_walks}, " 
                f"CloudCover: '{self._preferred_cloud_cover}', City: '{self._preferred_city}', "
                f"TimeRange: '{self._preferred_time_range}', Weights: {self.get_weights()})")