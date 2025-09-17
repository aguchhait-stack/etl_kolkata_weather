#!/bin/bash
# Navigate to ETL directory
cd /Users/arijitguchhait/Desktop/mydb/ETL || exit

# Run the ETL Python script
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 etl_kolkata_weather.py >> etl_weather.log 2>&1

# Force add files in case of .gitignore
git add -f kolkata_weather_plot.png etl_kolkata_weather.ipynb

# Commit with timestamp (allow empty commit if no changes)
git commit -m "Auto-update plot: $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Push to main branch
git push origin main --force >> push_log.log 2>&1

