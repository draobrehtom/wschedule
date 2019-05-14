# Installation

1. `pip install -r requirements.txt`
2. `pacman -S geckodriver`
3. `python app.py youridnumber yourpassword`
4. Find your schedule in `schedule.csv` file with app directory 

# Mandatory TODO
1) Power BI vizualization
 - Number of covered lectures and exercises 
 - Percentage bar by formula `covered_lectures / all_lectures` (same for exercises and total)
 - Ratio plot between subject / types / rooms

# Additional TODO
2) Notifications for mandatory classes
 - List of mandatory subjects
 - Exercises, Lecture or Lab
 - Set notification on schedule change in this week
3) Route to the University from calendar event
4) Useful information in event desctiption
 - Useful links per subject 


# Additional Info

credentials.json - is a configuration file of our gcalendar application 
(same as facebook has)

`sync result: 1m 20s (20s - pulling, 1m - sync with gcalendar)`
