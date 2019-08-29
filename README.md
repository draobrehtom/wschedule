# Installation

1. `pip install -r requirements.txt`
2. Download `geckodriver` from https://github.com/mozilla/geckodriver/releases/tag/v0.24.0
3. Install `Firefox Browser` and set `executable_path` inside `src/exporter.py` file at `line 35`
4. Run `python app.py 26477 fortheproject`
5. Wait for results and find our schedule in `schedule.csv` file inside directory 

# TODO
1) Notifications for mandatory classes
 - List of mandatory subjects
 - Exercises, Lecture or Lab
 - Set notification on schedule change in this week
2) Route to the University from calendar event
3) Useful information in event desctiption
 - Useful links per subject 


# Additional Info
credentials.json - is a configuration file of our gcalendar application 
(same as facebook has)

`sync result: 1m 20s (20s - pulling, 1m - sync with gcalendar)`
