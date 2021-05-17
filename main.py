#! /usr/bin/python3
# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime  # for reading present date
import requests  # for retreiving tzeva adom data from the Oref site
from plyer import notification  # for getting notification on your PC

#####################################################################
# To change city:
# go to line 22 and change the cities you desire to get an alert for
#####################################################################

resp = None
data = None
userInput = None
area = ['לציון', 'אשדוד', 'פלמחים', 'אשקלון', 'יבנה']

headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Referer': 'https://www.oref.org.il/12481-he/Pakar.aspx',
    'X-Requested-With': 'XMLHttpRequest',
}
while userInput != '-1':
    userInput = input('Enter cities names to get alerts for (in Hebrew) and press "Enter"'
                      '\nWhen you\'re done write "-1":')
    if userInput != '-1':
        area.insert(-1, userInput)

print("----------------\nThank you,\nyou'll get alerts for: ", ', '.join(area), "\n----------------")

while True:
    matchers = None
    try:
        resp = requests.get('https://www.oref.org.il/WarningMessages/alert/alerts.json', headers=headers).text
    except:
        print("Error: Can't get data from https://www.oref.org.il")
    if resp:
        data = json.loads(resp)['data']
        print(data)
        matchers = [d for d in data if any(xs in d for xs in area)]
        # print("matchers ", matchers, len(matchers))
        data = ', '.join(json.loads(resp)['data'])
        if len(matchers) > 0:
            notification.notify(
                # title of the notification
                title="צבע אדום",
                # the body of the notification
                message=datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "{redAlertsAreas}".format(
                    redAlertsAreas=data),
                # icon for the notification
                # (if you want to change it- notice it must be .ico file)
                app_icon='warning.ico',
                # the notification stays for 10sec
                timeout=10
            )
        else:
            print("Not in your list for alerts.")
    time.sleep(15)
