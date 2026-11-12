"""Pretend flights are taking off.

Every 2 seconds this script writes a small JSON file of departures into
incoming_flights/. The notebook reads that folder as a stream.

Run it in a JupyterLab terminal:  python flight_producer.py
Stop it with Ctrl+C.
"""

import random
import shutil
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

CSV = "/opt/spark/lesson-data/T_ONTIME_REPORTING.csv"
FOLDER = Path(__file__).parent / "incoming_flights"
SECONDS_BETWEEN_FILES = 2

flights = (
    pd.read_csv(CSV, usecols=["OP_CARRIER_FL_NUM", "ORIGIN", "ORIGIN_CITY_NAME", "DEST", "DEP_DELAY"])
    .dropna()
    .rename(columns={
        "OP_CARRIER_FL_NUM": "flight",
        "ORIGIN": "origin",
        "ORIGIN_CITY_NAME": "origin_city",
        "DEST": "dest",
        "DEP_DELAY": "dep_delay",
    })
)

shutil.rmtree(FOLDER, ignore_errors=True)
FOLDER.mkdir()
print(f"{len(flights)} flights loaded. A new file in {FOLDER} every {SECONDS_BETWEEN_FILES} seconds. Ctrl+C stops.")

try:
    while True:
        batch = flights.sample(random.randint(10, 60))
        now = datetime.now()
        batch.insert(0, "event_time", now.isoformat(timespec="seconds"))

        # Spark skips a file name it has already read, so the time in the name keeps every name new.
        name = f"flights_{now:%Y%m%d_%H%M%S}.json"
        # Spark ignores names that start with ".", so it never reads a half-written file.
        hidden = FOLDER / ("." + name)
        batch.to_json(hidden, orient="records", lines=True)
        hidden.rename(FOLDER / name)

        print(f"{name}: {len(batch)} departures")
        time.sleep(SECONDS_BETWEEN_FILES)
except KeyboardInterrupt:
    print("stopped")
