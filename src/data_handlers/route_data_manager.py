import pandas as pd
from src.models.route import Route
from src.models.user_preference import UserPreference
from src.utils.constants import DIFFICULTY_MULTIPLIERS, TIME_RANGES
import os


class RouteDataManager:
    def __init__(self, trails_csv_path: str):
        self._routes: list[Route] = []
        self._trails_csv_path = trails_csv_path
        self._load_routes_from_csv()
        print(f"Loaded {len(self._routes)} routes from CSV.")

    @property
    def routes(self) -> list[Route]:
        return self._routes

    def _load_routes_from_csv(self):
        if not os.path.exists(self._trails_csv_path):
            print(f"Błąd: Plik CSV '{self._trails_csv_path}' nie został znaleziony.")
            return

        try:
            df = pd.read_csv(self._trails_csv_path, sep=';', encoding='utf-16')
            print(f"Columns read from CSV (before mapping): {df.columns.tolist()}")

            column_mapping = {
                'Trail_Name': 'name',
                'City': 'region',
                'Trail_Length': 'length_km',
                'Difficulty': 'difficulty',
                'Rating': 'rating',
                'Link': 'link',
                'Photo': 'image_link'
            }
            df = df.rename(columns=column_mapping)

            required_cols_after_mapping = ['name', 'region', 'length_km', 'difficulty', 'rating', 'link', 'image_link']
            if not all(col in df.columns for col in required_cols_after_mapping):
                missing = [col for col in required_cols_after_mapping if col not in df.columns]
                print(f"Błąd: Po mapowaniu brak wymaganych kolumn w pliku CSV: {missing}.")
                print(f"Columns after attempted mapping: {df.columns.tolist()}")
                return

            if df.empty:
                print(f"Ostrzeżenie: Plik '{self._trails_csv_path}' jest pusty.")
                return

            for index, row in df.iterrows():
                try:
                    _id = index + 1
                    _name = str(row['name'])
                    _region = str(row['region'])
                    _length_km = float(str(row['length_km']).replace(' km', '').replace(',', '.'))
                    _difficulty = str(row['difficulty']).lower()
                    _rating_str = str(row['rating']).replace(',', '.')
                    _rating = 0.0 if _rating_str.lower() == 'brak ocen' else float(_rating_str)
                    _link = str(row['link'])
                    _image_link = str(row['image_link'])

                    route = Route(
                        id=_id, name=_name, region=_region, length_km=_length_km,
                        difficulty=_difficulty, rating=_rating, link=_link, image_link=_image_link
                    )
                    self._routes.append(route)
                except ValueError as e:
                    print(f"Błąd konwersji danych w wierszu {index + 1}: {e}. Wiersz: {row.to_dict()}")
                except KeyError as e:
                    print(f"Błąd klucza w wierszu {index + 1}: {e}. Sprawdź mapowanie. Wiersz: {row.to_dict()}")
        except pd.errors.EmptyDataError:
            print(f"Błąd: Plik '{self._trails_csv_path}' jest pusty.")
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas ładowania tras z '{self._trails_csv_path}': {e}")


    def check_route_match_preferences(self, route: Route, user_preferences: UserPreference) -> bool:
        """
        Sprawdza, czy dana trasa pasuje do preferencji użytkownika.
        route to obiekt klasy Route.
        user_preferences to obiekt klasy UserPreference.
        """
        difficulty_order = list(DIFFICULTY_MULTIPLIERS.keys())

        # .difficulty
        user_pref_idx = difficulty_order.index(user_preferences.preferred_difficulty)
        route_difficulty_idx = difficulty_order.index(route.difficulty)

        if route_difficulty_idx > user_pref_idx:
            return False

        # .length_km
        if not (user_preferences.min_length <= route.length_km <= user_preferences.max_length):
            return False

        # .rating
        if route.rating < user_preferences.min_rating:
            return False

        preferred_time_range_values = TIME_RANGES.get(user_preferences.preferred_time_range)
        if preferred_time_range_values:
            min_time, max_time = preferred_time_range_values
            # .estimated_time_hours (obliczone)
            if not (min_time <= route.estimated_time_hours <= max_time):
                return False

        # region
        if user_preferences.preferred_city != "Trójmiasto":  # "Trójmiasto" oznacza brak filtra miasta
            if route.region.lower() != user_preferences.preferred_city.lower():
                return False

        return True

    def filter_routes(self, user_preferences: UserPreference) -> list[Route]:
        filtered_routes = []
        for route_item in self._routes:
            if self.check_route_match_preferences(route_item, user_preferences):
                filtered_routes.append(route_item)
        print(f"Filtered down to {len(filtered_routes)} routes based on user preferences.")
        return filtered_routes

    def get_route_by_id(self, route_id: int) -> Route | None:
        for route in self._routes:
            if route.id == route_id:
                return route
        return None