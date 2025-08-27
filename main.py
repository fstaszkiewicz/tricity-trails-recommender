import os
from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.recommenders.route_recommender import RouteRecommender
from src.ui.user_interface import App

# ścieżka do pliku CSV z trasami
CSV_PATH = os.path.join("data", "trails.csv")

def main():

    if not os.path.exists(CSV_PATH):
        print(f"Nie znaleziono pliku z danymi o trasach: {CSV_PATH}")
        return

    # Inicjalizacja komponentów
    route_manager = RouteDataManager(trails_csv_path=CSV_PATH)
    weather_manager = WeatherDataManager()
    recommender = RouteRecommender(route_manager, weather_manager)

    # Uruchomienie aplikacji
    app = App(recommender=recommender)
    app.mainloop()

if __name__ == "__main__":
    main()