"""
data.py - ASTRAVITA data layer
-----------------------------------------------------------
ALL DATA IN THIS FILE IS SIMULATED (not real medical data).
Astronaut names are team members' names; all health data is simulated.

Team contract (do not rename without telling the team):
    get_astronauts()               -> list of dicts
    get_health_data(astronaut_id)  -> pandas DataFrame
-----------------------------------------------------------
"""

import numpy as np
import pandas as pd

# Number of simulated mission days
DAYS = 30


def get_astronauts():
    """Return the list of crew members (health data is simulated).

    "photo" is the path of an image file inside the "images" folder.
    If the file does not exist, the interface shows the initials instead.
    """
    return [
        {"id": "AST-01", "name": "Jafar Alrubaiy", "role": "Mission Commander",
         "age": 42, "mission": "ASTRAVITA-1", "mission_day": DAYS,
         "photo": "images/AST-01.jpg"},
        {"id": "AST-02", "name": "Mohammed Baqir", "role": "Flight Engineer",
         "age": 35, "mission": "ASTRAVITA-1", "mission_day": DAYS,
         "photo": "images/AST-02.jpg"},
        {"id": "AST-03", "name": "Ali Mohammed", "role": "Science Officer",
         "age": 33, "mission": "ASTRAVITA-1", "mission_day": DAYS,
         "photo": "images/AST-03.jpg"},
        {"id": "AST-04", "name": "Ali Hasan", "role": "Flight Surgeon",
         "age": 39, "mission": "ASTRAVITA-1", "mission_day": DAYS,
         "photo": "images/AST-04.jpg"},
        {"id": "AST-05", "name": "Taha Qasim", "role": "Mission Specialist",
         "age": 30, "mission": "ASTRAVITA-1", "mission_day": DAYS,
         "photo": "images/AST-05.jpg"},
    ]


def get_health_data(astronaut_id):
    """
    Return SIMULATED daily health data for one astronaut.

    Columns:
        date             - day of the mission
        heart_rate       - resting heart rate (bpm)
        sleep_hours      - hours of sleep
        activity_minutes - exercise minutes
        spo2             - blood oxygen (%)
        body_temp        - body temperature (C)
    """
    # Same astronaut -> same numbers every time (reproducible)
    seed = sum(ord(ch) for ch in astronaut_id)
    rng = np.random.default_rng(seed)

    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=DAYS)

    df = pd.DataFrame({
        "date": dates,
        "heart_rate": rng.normal(66, 3, DAYS).round(0),
        "sleep_hours": rng.normal(6.8, 0.4, DAYS).round(1),
        "activity_minutes": rng.normal(120, 12, DAYS).round(0),
        "spo2": rng.normal(97.6, 0.5, DAYS).clip(94, 100).round(1),
        "body_temp": rng.normal(36.7, 0.12, DAYS).round(2),
    })

    # Simulated change in the last 3 days for AST-02,
    # so the alerts page has something to detect later.
    if astronaut_id == "AST-02":
        df.loc[DAYS - 3:, "heart_rate"] += 14
        df.loc[DAYS - 3:, "sleep_hours"] -= 1.8

    # Smaller simulated change for AST-04 (a "warning", not "critical"):
    # blood oxygen a little lower than usual in the last 2 days.
    if astronaut_id == "AST-04":
        df.loc[DAYS - 2:, "spo2"] = [96.6, 96.4]

    return df
