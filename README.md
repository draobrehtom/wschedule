# Installation

**You should have Mozilla Firefox installed!**

[Presentation link](https://docs.google.com/presentation/d/1KmflMv4MoMv347rogEWM6tKwSy8gkSOlEDnevw8okhc/edit#slide=id.g60ff400cd6_0_209) - special thanks to @[veronicaverlan](https://github.com/veronicaverlan) (presentation), @[teoluna](https://github.com/teoluna) (vizualization) and @[thundera1z](https://github.com/thundera1z) (testing)
## Windows
`pip install -r requirements.txt`

## Linux
`pip install -r requirements.txt && chmod 755 geckodriver_linux`

## MacOS
`pip install -r requirements.txt && chmod 755 geckodriver_macos`

# Pulling schedule
**Execute `python app.py 26477 fortheproject`**


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
