#!/usr/bin/env python3

import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import os
import filecmp

# -----------------------
# Config
# -----------------------
DB_PATH = "/Users/arijitguchhait/Desktop/mydb/Database/weather.db"
TABLE_NAME = "kolkata_weather"
PLOT_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL/kolkata_weather.png"
HTML_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL/index.html"
REPO_PATH = "/Users/arijitguchhait/Desktop/mydb/ETL"

LATITUDE = 22.5726
LONGITUDE = 88.3639
API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m"

# -----------------------
# Fetch data
# -----------------------
response = requests.get(API_URL)
data = response.json()

df = pd.DataFrame({
    "timestamp": pd.to_datetime(data['hourly']['time']),
    "temperature": data['hourly']['temperature_2m']
})

# Save to SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
conn.close()
print(f"✅ Weather data loaded into {DB_PATH} | Rows: {len(df)} | Last timestamp: {df['timestamp'].max()}")

# -----------------------
# Plotting
# -----------------------
plt.figure(figsize=(10,5))
plt.plot(df['timestamp'], df['temperature'], marker='o')
plt.title("Kolkata Hourly Temperature")
plt.xlabel("Timestamp")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()

# TEMP plot file with explicit PNG format
TEMP_PLOT = PLOT_PATH + ".tmp"
plt.savefig(TEMP_PLOT, format='png')  # <-- FIXED HERE
plt.close()

# Only replace if plot changed
plot_changed = True
if os.path.exists(PLOT_PATH):
    plot_changed = not filecmp.cmp(TEMP_PLOT, PLOT_PATH, shallow=False)

if plot_changed:
    os.replace(TEMP_PLOT, PLOT_PATH)
    print(f"📊 Weather plot saved to {PLOT_PATH}")
else:
    os.remove(TEMP_PLOT)
    print("ℹ️ Plot unchanged")

# -----------------------
# Update index.html with latest timestamp
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
# Git commit & push
# -----------------------
os.chdir(REPO_PATH)
try:
    subprocess.run(["git", "add", "kolkata_weather.png", "index.html"], check=True)
    subprocess.run(["git", "commit", "-m", "Update weather plot"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("✅ Git commit & push completed")
except subprocess.CalledProcessError as e:
    print("⚠️ Git command failed or no changes to commit:", e)
