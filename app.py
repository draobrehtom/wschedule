import argparse
import csv
import src.gcalendar as gcalendar
import src.exporter as exporter
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    '--gcalendar', action='store_true'
)
parser.add_argument(
    'student_id'
)
parser.add_argument('password')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()


if args.debug:
    print("@ Debug mode")
    schedule = [
        {'description': '<a href="https://drive.google.com/open?id=1Vo-hdeJ2hQsbpWVMNWM1AzN2Z1fZgn6l" target="_blank">Book</a>', 
        'date': datetime.datetime.now().strftime("%Y-%m-%d"), 'from': '08:00', 'to': '11:10', 
        'subject': 'German', 
        'mandatory': True, 
        'teacher': 'mgr Katarzyna Wójcik', 
        'classroom': '420', 'type': 'LE', 'location': 'ul. Cieplaka 1c, 41-300 Dąbrowa Górnicza',
        'submit': 'Pass with grade'}
        ]
    gcalendar.synchronize(schedule, calendarname="qqq")
    exit(0)

student_id = args.student_id
password = args.password


#Read JSON data into the datastore variable
with open('subjects.json', 'r') as f:
    subject_descriptions = json.load(f)

schedule = exporter.get_schedule(student_id, password, subject_descriptions)

if args.gcalendar:
    print("Schedule retrieved. Synchronization with Google Calendar ... ")
    calendarname = "Data Scientist" # is not "primary"
    gcalendar.synchronize(schedule, calendarname)
else:
    print('Exporing your schedule into csv file ... ')
    with open('schedule.csv', 'w') as schedule_file:
        writer = csv.DictWriter(schedule_file, fieldnames=schedule.get_header())
        writer.writeheader()
        for row in schedule.get_body():

            # Filtration
            if row['classroom'] == 'AUD D':
                continue


            date_from = row['date'] + ' ' + row['from']
            date_to = row['date'] + ' ' + row['to']

            import datetime
            time1 = datetime.datetime.strptime(row['to'], "%H:%M")
            time2 = datetime.datetime.strptime(row['from'], "%H:%M")
            diff = time1 -time2
            row['hours'] = round(diff.total_seconds() / 3600, 2)
            writer.writerow(row)

print('Done')