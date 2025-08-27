# src/ui/user_interface.py

import customtkinter as ctk
import webbrowser
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO

from src.recommenders.route_recommender import RouteRecommender
from src.models.user_preference import UserPreference
from src.utils.constants import TIME_RANGES, LENGTH_OPTIONS, TRICITY_COORDS, DIFFICULTY_MULTIPLIERS, \
    CLOUD_COVER_PREFERENCES

# Ustawienie wyglądu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self, recommender: RouteRecommender):
        super().__init__()
        self.recommender = recommender

        self.title("Recommender Tras Spacerowych")
        self.geometry("1400x900")

        self.grid_columnconfigure(0, weight=1, minsize=320)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self._create_filter_frame()
        self._create_results_frame()

    def _update_rating_label(self, value):
        self.rating_value_label.configure(text=f"{value:.1f} ⭐")

    def _update_min_temp_label(self, value):
        self.min_temp_value_label.configure(text=f"{int(value)}°C")

    def _update_max_temp_label(self, value):
        self.max_temp_value_label.configure(text=f"{int(value)}°C")

    # Metoda do formatowania czasu
    def _format_time(self, total_hours: float) -> str:
        """Konwertuje godziny w formacie dziesiętnym (np. 2.79) na format 'Xh Ym'."""
        if total_hours < 0:
            return "0m"

        hours = int(total_hours)
        minutes = round((total_hours - hours) * 60)

        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"

    def _create_filter_frame(self):
        # Ta metoda pozostaje bez zmian
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(filter_frame, text="Filtry Tras", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10, padx=10)

        self.widgets = {}

        difficulty_options =list(DIFFICULTY_MULTIPLIERS.keys())
        ctk.CTkLabel(filter_frame, text="Poziom trudności:").pack(padx=10, anchor="w")
        self.widgets['difficulty'] = ctk.CTkOptionMenu(filter_frame, values=difficulty_options)
        self.widgets['difficulty'].pack(padx=10, pady=(0, 10), fill="x")

        time_options = list(TIME_RANGES.keys())
        ctk.CTkLabel(filter_frame, text="Czas przejścia:").pack(padx=10, anchor="w")
        self.widgets['time'] = ctk.CTkOptionMenu(filter_frame, values=time_options)
        self.widgets['time'].pack(padx=10, pady=(0, 10), fill="x")

        len_str_options = [str(x) for x in LENGTH_OPTIONS]
        ctk.CTkLabel(filter_frame, text="Min długość (km):").pack(padx=10, anchor="w")
        self.widgets['min_len'] = ctk.CTkOptionMenu(filter_frame, values=len_str_options)
        self.widgets['min_len'].pack(padx=10, pady=(0, 10), fill="x")
        ctk.CTkLabel(filter_frame, text="Max długość (km):").pack(padx=10, anchor="w")
        self.widgets['max_len'] = ctk.CTkOptionMenu(filter_frame, values=len_str_options)
        self.widgets['max_len'].set(len_str_options[-1])
        self.widgets['max_len'].pack(padx=10, pady=(0, 10), fill="x")

        rating_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        rating_frame.pack(fill="x", padx=10, pady=(0, 10))
        rating_frame.grid_columnconfigure(0, weight=1)
        rating_frame.grid_columnconfigure(1, weight=3)
        ctk.CTkLabel(rating_frame, text="Minimalna ocena:").grid(row=0, column=0, sticky="w")
        self.rating_value_label = ctk.CTkLabel(rating_frame, text="3.0 ⭐")
        self.rating_value_label.grid(row=0, column=1, sticky="e", padx=(0, 5))
        self.widgets['rating'] = ctk.CTkSlider(rating_frame, from_=0, to=5, number_of_steps=50,
                                               command=self._update_rating_label)
        self.widgets['rating'].set(3.0)
        self.widgets['rating'].grid(row=1, column=0, columnspan=2, sticky="ew")

        city_options = ["Trójmiasto"] + list(TRICITY_COORDS.keys())
        ctk.CTkLabel(filter_frame, text="Miasto:").pack(padx=10, anchor="w")
        self.widgets['city'] = ctk.CTkOptionMenu(filter_frame, values=sorted(list(set(city_options))))
        self.widgets['city'].pack(padx=10, pady=(0, 10), fill="x")

        ctk.CTkLabel(filter_frame, text="Twoje Preferencje", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        cloud_map = {'Bezchmurnie': 'bezchmurnie', 'Lekkie zachmurzenie': 'troche_chmur',
                     'Pełne zachmurzenie': 'pelne_zachmurzenie'}
        ctk.CTkLabel(filter_frame, text="Preferowane zachmurzenie:").pack(padx=10, anchor="w")
        self.widgets['cloud_cover'] = ctk.CTkOptionMenu(filter_frame, values=list(cloud_map.keys()),
                                                        variable=ctk.StringVar(value='Lekkie zachmurzenie'))
        self.widgets['cloud_cover_map'] = cloud_map
        self.widgets['cloud_cover'].pack(padx=10, pady=(0, 10), fill="x")

        min_temp_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        min_temp_frame.pack(fill="x", padx=10, pady=(0, 10))
        min_temp_frame.grid_columnconfigure(0, weight=1)
        min_temp_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(min_temp_frame, text="Min temp:").grid(row=0, column=0, sticky="w")
        self.min_temp_value_label = ctk.CTkLabel(min_temp_frame, text="-5°C")
        self.min_temp_value_label.grid(row=0, column=1, sticky="e")
        self.widgets['min_temp'] = ctk.CTkSlider(min_temp_frame, from_=-20, to=40, number_of_steps=60,
                                                 command=self._update_min_temp_label)
        self.widgets['min_temp'].set(-5)
        self.widgets['min_temp'].grid(row=1, column=0, columnspan=2, sticky="ew")

        max_temp_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        max_temp_frame.pack(fill="x", padx=10, pady=(0, 10))
        max_temp_frame.grid_columnconfigure(0, weight=1)
        max_temp_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(max_temp_frame, text="Max temp:").grid(row=0, column=0, sticky="w")
        self.max_temp_value_label = ctk.CTkLabel(max_temp_frame, text="25°C")
        self.max_temp_value_label.grid(row=0, column=1, sticky="e")
        self.widgets['max_temp'] = ctk.CTkSlider(max_temp_frame, from_=-20, to=40, number_of_steps=60,
                                                 command=self._update_max_temp_label)
        self.widgets['max_temp'].set(25)
        self.widgets['max_temp'].grid(row=1, column=0, columnspan=2, sticky="ew")

        self.widgets['night_walks'] = ctk.CTkCheckBox(filter_frame, text="Lubisz nocne spacery?")
        self.widgets['night_walks'].pack(padx=10, pady=10, anchor="w")

        self.widgets['precip'] = ctk.CTkCheckBox(filter_frame, text="Przeszkadzają Ci opady?", onvalue=True,
                                                 offvalue=False)
        self.widgets['precip'].select()
        self.widgets['precip'].pack(padx=10, pady=10, anchor="w")

        apply_button = ctk.CTkButton(filter_frame, text="Wyszukaj Trasy", command=self._apply_filters)
        apply_button.pack(padx=10, pady=20, fill="x", side="bottom")

    def _create_results_frame(self):
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Dostępne Trasy")
        self.results_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def _apply_filters(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        diff = self.widgets['difficulty'].get()
        time_r = self.widgets['time'].get()

        pref_diff = diff if diff != "Dowolna" else 'hard'
        pref_time = time_r if time_r != "Dowolny" else "powyżej 8 godzin"

        cloud_display_val = self.widgets['cloud_cover'].get()
        pref_cloud = self.widgets['cloud_cover_map'][cloud_display_val]

        min_temp_val = self.widgets['min_temp'].get()
        max_temp_val = self.widgets['max_temp'].get()

        if min_temp_val > max_temp_val:
            min_temp_val, max_temp_val = max_temp_val, min_temp_val

        prefs = UserPreference(
            preferred_difficulty=pref_diff.lower(),
            preferred_time_range=pref_time,
            min_length=float(self.widgets['min_len'].get()),
            max_length=float(self.widgets['max_len'].get()),
            min_rating=self.widgets['rating'].get(),
            preferred_city=self.widgets['city'].get(),
            allow_night_walks=bool(self.widgets['night_walks'].get()),
            allow_precipitation=not bool(self.widgets['precip'].get()),
            preferred_cloud_cover=pref_cloud,
            min_temp=min_temp_val,
            max_temp=max_temp_val
        )

        filtered_routes = self.recommender.filter_routes(prefs)

        if not filtered_routes:
            ctk.CTkLabel(self.results_frame, text="Brak tras spełniających kryteria.").pack(pady=20)
            return

        for route in filtered_routes:
            self._display_route(route, prefs)

    def _display_route(self, route, prefs):
        # Ta metoda została lekko zmodyfikowana
        route_frame = ctk.CTkFrame(self.results_frame)
        route_frame.pack(padx=10, pady=10, fill="x")

        top_frame = ctk.CTkFrame(route_frame, fg_color="transparent")
        top_frame.pack(padx=10, pady=10, fill="x")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=3)

        img_label = ctk.CTkLabel(top_frame, text="Ładowanie...")
        img_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="nw")
        threading.Thread(target=self._load_image, args=(route.image_link, img_label), daemon=True).start()

        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(info_frame, text=route.name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame,
                     text=f"Region: {route.region} | Trudność: {route.difficulty.capitalize()} | Ocena: {route.rating} ⭐").pack(
            anchor="w")

        # === POCZĄTEK ZMIAN: Użycie nowej metody formatowania czasu ===
        formatted_time = self._format_time(route.estimated_time_hours)
        ctk.CTkLabel(info_frame, text=f"Długość: {route.length_km} km | Szacowany czas: {formatted_time}").pack(
            anchor="w")
        # === KONIEC ZMIAN ===

        ctk.CTkButton(info_frame, text="Otwórz w AllTrails", command=lambda u=route.link: self._open_link(u)).pack(
            anchor="w", pady=5)

        comfort_data = self.recommender.calculate_daily_comfort_for_route(route, prefs)
        calendar_frame = ctk.CTkFrame(route_frame)
        calendar_frame.pack(fill="x", padx=10, pady=(0, 10))

        for i, day_data in enumerate(comfort_data):
            col = i % 7
            row = i // 7
            day_frame = ctk.CTkFrame(calendar_frame, fg_color=day_data['color'])
            day_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(day_frame, text=day_data['date'].strftime('%d.%m'),
                         font=ctk.CTkFont(size=12, weight="bold")).pack()
            ctk.CTkLabel(day_frame, text=f"{day_data['score']}%").pack()
            calendar_frame.grid_columnconfigure(col, weight=1)

    def _open_link(self, url):
        webbrowser.open_new_tab(url)

    def _load_image(self, url, label_widget):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img_data = response.content

            pil_image = Image.open(BytesIO(img_data))
            ctk_image = ctk.CTkImage(pil_image, size=(250, 150))

            self.after(0, lambda: label_widget.configure(image=ctk_image, text=""))
        except Exception as e:
            print(f"Error loading image: {e}")
            self.after(0, lambda: label_widget.configure(text="Błąd obrazu"))