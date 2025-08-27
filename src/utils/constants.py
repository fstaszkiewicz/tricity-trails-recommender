import datetime

# Bazowa prędkość w km/h dla obliczania czasu przejścia
BASE_WALKING_SPEED_KMH = 4.7



# Mnożniki trudności dla obliczania czasu przejścia
DIFFICULTY_MULTIPLIERS = {
    'easy': 1.0,
    'moderate': 1.3,
    'hard': 1.6
}

# Zakresy czasowe dla filtrowania tras
TIME_RANGES = {
    "dowolny": (0, float('inf')),
    "do 2 godzin": (0, 2),
    "2-4 godziny": (2, 4),
    "4-6 godziny": (4, 6),
    "6-8 godziny": (6, 8),
    "powyżej 8 godzin": (8, float('inf'))
}

# Opcje długości trasy dla filtrowania
LENGTH_OPTIONS = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50]

# Maksymalna ocena trasy
MAX_RATING = 5.0

# Progi procentowe dla kolorów komfortu (0-100)
COMFORT_COLOR_THRESHOLDS = {
    'green': 80,    # >= 80
    'yellow': 60,   # >= 60 i < 80
    'orange': 40,   # >= 40 i < 60
    'red': 0        # < 40
}

# Preferencje zachmurzenia - mapowanie na zakresy wartości cloud_cover (0-100%)
CLOUD_COVER_PREFERENCES = {
    'bezchmurnie': (0, 30),      # Niskie zachmurzenie
    'troche_chmur': (30, 70),    # Umiarkowane zachmurzenie
    'pelne_zachmurzenie': (70, 100) # Wysokie zachmurzenie
}

# Centralne koordynaty dla miast Trójmiasta
TRICITY_COORDS = {
    "Gdańsk": {"latitude": 54.372158, "longitude": 18.646352},
    "Gdynia": {"latitude": 54.518882, "longitude": 18.530514},
    "Sopot": {"latitude": 54.444760, "longitude": 18.556272},
    "Trójmiasto": {"latitude": 54.4452, "longitude": 18.5603} # Środek Trójmiasta
}

# Godziny nocne, które mogą być wykluczone z obliczeń komfortu
NIGHT_HOURS = list(range(22, 24)) + list(range(0, 5))

# Dni prognozy
FORECAST_DAYS = 14