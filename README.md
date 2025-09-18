## 📊 Latest Weather Plot

![Kolkata Weather Forecast](https://aguchhait-stack.github.io/etl_kolkata_weather/kolkata_weather.png?ts=20250924_2300)

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


