#!/usr/bin/env python3

import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import os

# -----------------------
# Config
# -----------------------
DB_PATH = "/Users/arijitguchhait/Desktop/mydb/Database/weather.db"
TABLE_NAME = "kolkata_weather"
DOCS_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL/docs"
PLOT_PATH = os.path.join(DOCS_PATH, "kolkata_weather.png")
HTML_PATH = os.path.join(DOCS_PATH, "index.html")
README_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL/README.md"
REPO_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL"

LATITUDE = 22.5726
LONGITUDE = 88.3639
API_URL = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,relativehumidity_2m"
)

# -----------------------
# Fetch data
# -----------------------
response = requests.get(API_URL)
data = response.json()

df = pd.DataFrame({
    "timestamp": pd.to_datetime(data['hourly']['time']),
    "temperature": data['hourly']['temperature_2m'],
    "humidity": data['hourly']['relativehumidity_2m']
})

# Save to SQLite
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
conn.close()
print(f"✅ Weather data loaded into {DB_PATH} | Rows: {len(df)} | Last timestamp: {df['timestamp'].max()}")

# -----------------------
# Plotting with footer embedded
# -----------------------
fig, ax1 = plt.subplots(figsize=(12,6))

# Temperature (red)
ax1.plot(df['timestamp'], df['temperature'], 'r-o', label="Temperature (°C)")
ax1.set_xlabel("Timestamp")
ax1.set_ylabel("Temperature (°C)", color='r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.grid(True, which='major', axis='both', linestyle='--', alpha=0.5)

# Humidity (blue) on secondary axis
ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['humidity'], 'b-s', label="Humidity (%)")
ax2.set_ylabel("Humidity (%)", color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', framealpha=0.9)

# Title
plt.title("Kolkata Hourly Temperature & Humidity")
plt.xticks(rotation=45)

# Footer inside PNG
plt.figtext(0.5, 0.01, "© 2025 Created by Arijit Guchhait", ha="center", fontsize=10, color="gray")

# Save plot
os.makedirs(DOCS_PATH, exist_ok=True)
plt.savefig(PLOT_PATH, format='png', bbox_inches='tight')
plt.close()
print(f"📊 Weather plot saved to {PLOT_PATH}")

# -----------------------
# Update index.html
# -----------------------
last_ts = df['timestamp'].max()
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Kolkata 7-Day Weather Forecast</title>
  <style>
    body {{ font-family: Arial, sans-serif; text-align: center; margin: 40px; }}
    footer {{ margin-top: 40px; font-size: 14px; color: #555; }}
  </style>
</head>
<body>
  <h1>Kolkata 7-Day Hourly Weather Forecast</h1>
  <p>Last updated: {last_ts}</p>
  <img src="kolkata_weather.png?ts={last_ts.strftime('%Y%m%d_%H%M')}" alt="Weather Forecast" width="1000">
  <footer>© 2025 Created by <strong>Arijit Guchhait</strong></footer>
</body>
</html>
"""
with open(HTML_PATH, "w") as f:
    f.write(html_content)
print(f"✅ index.html updated with latest timestamp")

# -----------------------
# Update README.md
# -----------------------
readme_content = f"""
## 📊 Latest Weather Plot

![Kolkata Weather Forecast](https://aguchhait-stack.github.io/etl_kolkata_weather/kolkata_weather.png?ts={last_ts.strftime('%Y%m%d_%H%M')})

# ETL Kolkata Weather

This repository contains an ETL pipeline that extracts hourly weather data for Kolkata,
transforms it, loads it into an SQLite database, and generates plots. 

The ETL runs automatically every hour using a cron job and pushes updates to GitHub.

## Files

- `etl_kolkata_weather.ipynb` - Jupyter Notebook for ETL.
- `etl_kolkata_weather.py` - Converted Python script.
- `kolkata_weather.png` - Generated plot (temperature & humidity with footer).
- `run_etl_and_push.sh` - Script to run ETL and push updates to GitHub.
- `push_plot.sh` - Git push script.

Check the live site here: [Kolkata 7-Day Weather Forecast](https://aguchhait-stack.github.io/etl_kolkata_weather/)
"""
with open(README_PATH, "w") as f:
    f.write(readme_content)
print(f"✅ README.md updated with latest PNG link")

# -----------------------
# Git commit & push
# -----------------------
os.chdir(REPO_PATH)
try:
    subprocess.run(["git", "add", "docs/kolkata_weather.png", "docs/index.html", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Update weather plot with temperature, humidity, and footer"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("✅ Git commit & push completed")
except subprocess.CalledProcessError as e:
    print("⚠️ Git command failed or no changes to commit:", e)
