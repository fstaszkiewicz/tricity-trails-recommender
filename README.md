# Tricity Trails Recommender 

![Application Screenshot](https://github.com/fstaszkiewicz/tricity-trails-recommender/blob/main/assets/app_screenshot.png?raw=true)

## Project Goal

The goal of this project was to build a simple yet functional desktop application in Python. It serves to demonstrate key skills in object-oriented programming, external API integration, and graphical user interface (GUI) development. The application implements a trail recommendation system based on user preferences and weather data.
## Functionality Overview

The **Tricity Trails Recommender** application allows users to find walking and running trails in the Tricity area (Gdańsk, Sopot, Gdynia). A user can define their preferences, such as location, trail length, or difficulty level. A key feature is the integration with a weather API, which enables the assessment of the "comfort level" for a walk on each trail over the next 7 days.

### Key Implemented Features:

* **Multi-criteria trail filtering** based on attributes like:
    * Location (Gdańsk, Sopot, Gdynia)
    * Length and estimated time
    * Difficulty level
    * Minimum rating
* **Integration with the Open-Meteo API** to fetch weather forecasts.
* **A weather comfort scoring algorithm** that analyzes factors such as temperature, precipitation, and cloud cover to assign a daily attractiveness score to each trail.
* **A dynamic user interface** (built with `CustomTkinter`) that visualizes recommendations and a 7-day comfort calendar for each trail.
* **Data handling** from a CSV file using the `Pandas` library.

## Architecture and Workflow

The project is built on object-oriented principles, with a clear separation of modules responsible for business logic, data handling, and presentation.

1.  **Data Management:**
    * `RouteDataManager`: Responsible for loading and parsing trail data from the `trails.csv` file.
    * `WeatherDataManager`: Communicates with the Open-Meteo API, using `requests-cache` to optimize queries.
2.  **Recommendation Engine (`RouteRecommender`):**
    * Filters trails according to user preferences defined in the GUI.
    * Calculates a personalized "weather comfort" score for each matching trail, considering the weights assigned to various criteria.
    * Sorts the results and passes them to the presentation layer.
3.  **User Interface (`UserInterface`):**
    * Built with `CustomTkinter`, allowing for intuitive input of preferences.
    * Presents the results in a clean, scrollable list, dynamically generating a view for each trail along with its weather calendar.

## Technologies Used

* **Language:** Python 3.10+
* **GUI:** CustomTkinter
* **Data Handling:** Pandas
* **HTTP Communication:** Requests, Requests-Cache, Retry-Requests
* **API:** Open-Meteo Weather API
* **Image Handling:** Pillow 

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/fstaszkiewicz/tricity-trails-recommender.git
    cd tricity-trails-recommender
    ```

2.  **Create and activate a virtual environment** (recommended):

    ```bash
    # Step 1: Create the environment 
    # On Windows
    python -m venv venv
    
    # On macOS/Linux (using python3 is safer)
    python3 -m venv venv

    # Step 2: Activate the environment 
    # On Windows
    .\venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```