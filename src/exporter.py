from selenium import webdriver
from time import sleep
import datetime

class Schedule:
    header = [
        'description','date',
        'from','to',
        'subject','mandatory','teacher','classroom','type','location',
        'submit'
    ]
    body = []

    def __init__(self, body, header=header):
        self.set_header(header)
        self.set_body(body)

    def set_header(self, header):
        self.header = header

    def set_body(self, body):
        self.body = body

    def get_header(self):
        return self.header
    
    def get_body(self):
        return self.body


def get_schedule(student_id, password, subject_descriptions):
    options = webdriver.FirefoxOptions()
    # options.set_headless()
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(1120, 550)
    browser.get('https://wu.wsb.edu.pl')

    browser.implicitly_wait(5)
    login_input = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_MiddleContentPlaceHolder_txtIdent')
    password_input = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_MiddleContentPlaceHolder_txtHaslo')
    submit_button = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_MiddleContentPlaceHolder_butLoguj')

    login_input.send_keys(student_id)
    password_input.send_keys(password)
    submit_button.click()

    browser.get('https://wu.wsb.edu.pl/WU/PodzGodzin.aspx')
    semestralnie = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_RightContentPlaceHolder_rbJak_2')
    semestralnie.click()

    schedule = browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_RightContentPlaceHolder_dgDane')

    rows = browser.find_elements_by_xpath('/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')
    cols = browser.find_elements_by_xpath('/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/table/tbody/tr[1]/*')

    print("No of schedule columns are: %s" % len(cols))
    print("No of schedule rows are: %s" % len(rows))



    # 'description': '<a href="https://docs.google.com/presentation/d/17DWZTD-fh95xXFVEd7co6YdQti5WeiujcOtHUNEHcDo/edit?usp=sharing" target="_blank">Presentation</a>'
    # 'description': '<a href="https://drive.google.com/open?id=1Vo-hdeJ2hQsbpWVMNWM1AzN2Z1fZgn6l" target="_blank">Book</a>'

    reasons = {
        'Odwołane': 'Canceled'
    }

    # 0 - type
    # 1 - date and day of week
    # 2 - from 
    # 3 - to 
    # 4 - subject
    # 5 - teacher
    # 6 - classroom
    # 7 - type 1
    # 8 - adress 
    # 9 - type 2
    # 10 - submit


    schedule = []
    sch_row = {'date': None, 'from': None, 'to': None, 'subject': None}

    for i in range(2, len(rows)):
        row_data = {
            'description': ''
        }
        for j in range(1, len(cols) + 1):
            cell = browser.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/table/tbody/tr[%s]/*[%s]' % (i, j))
            data = cell.text

            if j == 2:
                # 08.03.2019 -> 2019-03-16
                # 0000.00.00 wtorek
                data = data.split(' ')[0].split('.')
                row_data['date'] = "%s-%s-%s" % (data[2],data[1],data[0],)
            elif j == 3:
                row_data['from'] = data
            elif j == 4:
                row_data['to'] = data
            elif j == 5:
                row_data['subject'] = data
                if subject_descriptions.get(data):
                    row_data['mandatory'] = subject_descriptions[data]['mandatory']
                    row_data['subject'] = subject_descriptions[data]['en']
                    row_data['description'] = subject_descriptions[data].get('description', '')
            elif j == 6:
                row_data['teacher'] = data
            elif j == 7:
                data = data.split('DG ')
                row_data['classroom'] = data[0] + data[1]
                row_data['classroom'] = reasons.get(row_data['classroom'], row_data['classroom'])
            elif j == 8:
                if data == "J":
                    data = "LE"
                elif data == "W":
                    data = "L"
                elif data == "ĆW":
                    data = "E"

                row_data['type'] = data
            elif j == 9:
                row_data['location'] = data
            elif j == 11:
                if data == "Zal. z oceną":
                    data = "Pass with grade"
                elif data == "Zaliczenie":
                    data = "Pass"
                elif data == "Egzamin":
                    data = "Exam"
                row_data['submit'] = data

        schedule.append(row_data)

    browser.close()

    return Schedule(schedule)
