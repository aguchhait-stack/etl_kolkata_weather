#!/bin/bash
# Navigate to repo
cd /Users/arijitguchhait/Desktop/mydb/ETL

# Run ETL script
/usr/bin/env python3 etl_kolkata_weather.py

# Copy updated plot into docs folder for GitHub Pages
cp kolkata_weather.png docs/kolkata_weather.png

# Add changed files (plot + docs)
git add kolkata_weather.png docs/kolkata_weather.png docs/index.html etl_kolkata_weather.py

# Check if there are changes before committing
if [ -n "$(git status --porcelain)" ]; then
  git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
  echo "$(date): pushed updates" >> push_log.log
else
  echo "$(date): no changes, push skipped" >> push_log.log
fi
#!/bin/bash
# Navigate to repo
cd /Users/arijitguchhait/Desktop/mydb/ETL

# Run ETL script
/usr/bin/env python3 etl_kolkata_weather.py

# Add changed files (plot + log + db if you want)
git add kolkata_weather.png etl_kolkata_weather.py

# Check if there are changes before committing
if [ -n "$(git status --porcelain)" ]; then
  git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
  echo "$(date): pushed updates" >> push_log.log
else
  echo "$(date): no changes, push skipped" >> push_log.log
fi
#!/bin/bash

cd /Users/arijitguchhait/Desktop/mydb/ETL || exit

# Run ETL
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 etl_kolkata_weather.py >> etl_weather.log 2>&1

# Git push
git add -f kolkata_weather_plot.png etl_kolkata_weather.ipynb
git commit -m "Auto-update plot: $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty
git push origin main --force >> push_log.log 2>&1
#!/bin/bash

# Navigate to ETL directory
cd /Users/arijitguchhait/Desktop/mydb/ETL || exit

# Run the ETL Python script
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 etl_kolkata_weather.py >> etl_weather.log 2>&1

# Force add files (ignore .gitignore)
git add -f kolkata_weather_plot.png etl_kolkata_weather.ipynb

# Commit with timestamp (allow empty commit if no changes)
git commit -m "Auto-update plot: $(date '+%Y-%m-%d %H:%M:%S')" --allow-empty

# Push to main branch
git push origin main --force >> push_log.log 2>&1
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

