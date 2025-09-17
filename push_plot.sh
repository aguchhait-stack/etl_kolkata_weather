#!/bin/bash
# Navigate to ETL directory
cd /Users/arijitguchhait/Desktop/mydb/ETL || exit

# Add files (force add in case of .gitignore)
git add -f kolkata_weather_plot.png etl_kolkata_weather.ipynb

# Commit with timestamp
git commit -m "Auto-update plot: $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Push to main branch
git push origin main --force

