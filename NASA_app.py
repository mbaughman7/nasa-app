import requests
from datetime import datetime
import tkinter
# from nasa_data import data


response = requests.get("https://api.nasa.gov/DONKI/CME?api_key=DEMO_KEY")
data = response.json()
print(data)
cme_list = []

for item in data:
    try:
        earth_hit = item["cmeAnalyses"][0]["enlilList"][0]["estimatedShockArrivalTime"]
    except TypeError:
        pass
        # print("error here.  Probably a null")
    else:
        if earth_hit:
            name = item["activityID"]
            impact_time = item["cmeAnalyses"][0]["enlilList"][0]["estimatedShockArrivalTime"]
            clean_time_date = impact_time.split("T")[0]
            clean_time = impact_time.split("T")[1].split("Z")[0]
            entry = f"CME identified as {name} will impact earth on {clean_time_date} at approx {clean_time}"
            cme_list.append(entry)
### FOR TROUBLESHOOTING
# for i in enumerate(cme_list):
#     print(i)
try:
    with open("CME_events.txt",'r') as my_file:
        cme_events = my_file.readlines()
        ### FOR TROUBLESHOOTING
        # for line in cme_events:
        #     print(f"this is from file: {line}")
    with open("CME_events.txt",'w') as my_file:
        for item in cme_list:
            if item in cme_events:
                continue
            my_file.write('%s\n' % item)
            print(item)
            
except FileNotFoundError:
    with open("CME_events.txt",'w') as my_file:
        my_file.write("")
        
#TODO this part needs to be cleaned up.  As written, the first time the program is run,
# it will simply create a file and then exit.  



# Create button that executes the GET request (no parameters, at first)


