from src.utils.constants import BASE_WALKING_SPEED_KMH, DIFFICULTY_MULTIPLIERS, TIME_RANGES
import datetime

class Route:
    # id generowane w RouteDataManager
    def __init__(self, id: int, name: str, region: str, length_km: float,
                 difficulty: str, rating: float, link: str,
                 image_link: str):  # 'id' jest teraz jako argument, bo jest przekazywane
        if not isinstance(id, int) or id < 0:  # Walidacja id nadal potrzebna, bo jest przekazywane
            raise ValueError("ID musi być nieujemną liczbą całkowitą.")
        if not isinstance(name, str) or not name:
            raise ValueError("Nazwa trasy nie może być pusta.")
        if not isinstance(region, str) or not region:
            raise ValueError("Region trasy nie może być pusty.")
        if not isinstance(length_km, (int, float)) or length_km <= 0:
            raise ValueError("Długość trasy musi być dodatnią liczbą.")
        if difficulty not in DIFFICULTY_MULTIPLIERS:
            raise ValueError(
                f"Nieznana trudność trasy: {difficulty}. Dopuszczalne: {list(DIFFICULTY_MULTIPLIERS.keys())}")
        if not isinstance(rating, (int, float)) or not (0 <= rating <= 5):
            raise ValueError("Ocena trasy musi być liczbą od 0 do 5.")
        if not isinstance(link, str) or not link:
            raise ValueError("Link do trasy nie może być pusty.")
        if not isinstance(image_link, str) or not image_link:
            raise ValueError("Link do zdjęcia nie może być pusty.")

        self._id = id
        self._name = name
        self._region = region
        self._length_km = length_km
        self._difficulty = difficulty
        self._rating = rating
        self._link = link
        self._image_link = image_link
        self._estimated_time_hours = self._calculate_estimated_time()

    @property
    def id(self) -> int:
        return self._id # Przykład publicznego dostęp do odczytu

    @property
    def name(self) -> str:
        return self._name

    @property
    def region(self) -> str:
        return self._region

    @property
    def length_km(self) -> float:
        return self._length_km

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def link(self) -> str:
        return self._link

    @property
    def image_link(self) -> str:
        return self._image_link

    @property
    def estimated_time_hours(self) -> float:
        return self._estimated_time_hours

    def _calculate_estimated_time(self) -> float:
        """
        Szacuje czas przejścia trasy na podstawie długości i trudności.
        """
        difficulty_multiplier = DIFFICULTY_MULTIPLIERS.get(self._difficulty.lower(), 1.0)
        return (self._length_km * difficulty_multiplier) / BASE_WALKING_SPEED_KMH

    def __repr__(self):
        return (f"Route(ID: {self._id}, Name: '{self._name}', Region: '{self._region}', "
                f"Length: {self._length_km:.2f}km, Difficulty: '{self._difficulty}', "
                f"Rating: {self._rating:.1f}, Est. Time: {self._estimated_time_hours:.2f}h)")