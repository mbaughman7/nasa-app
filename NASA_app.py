import requests
from datetime import datetime
from tkinter import *
from tkinter import messagebox
# from nasa_data import data

#-------------------------DATA RETRIEVAL FROM API--------------------------------------------
def retrieve_data():
    response = requests.get("https://api.nasa.gov/DONKI/CME?api_key=DEMO_KEY")
    code = response.status_code
    print(f"GET request sent.  status code of {code} returned")

    response.raise_for_status()
    raw_data = response.json()
    return raw_data
#--------------------------------------------------------------------------------------------



#-------------------------GENERATE CLEAN LIST OF CMEs THAT WILL HIT EARTH-----------------------------------

def generate_cme_list():

    data = retrieve_data()
    #FOR TROUBLESHOOTING
    print("data retrieved")
    print(data)

    new_list = []

    for item in data:
        try:
            earth_hit = item["cmeAnalyses"][0]["enlilList"][0]["estimatedShockArrivalTime"]
            #if the CME is going to hit Earth, it will have an estimated shock arrival time.  otherwise, it will be 'none' and will return a type error
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
                new_list.append(entry)
    print("all done creating new CME list")

    return new_list
    ### FOR TROUBLESHOOTING
    # for i in enumerate(cme_list):
    #     print(i)

#-------------------------------------------------------------------------------------------------------------



#----------------OPEN/GENERATE CME TEXT FILE--READ CMEs FROM IT--UPDATE FILE WITH CMEs NOT ALREADY PRESENT----

def update_text_file():
    cme_list = generate_cme_list()
    try:
        with open("CME_events.txt",'r') as my_file:
            cme_events = my_file.readlines()
            ### FOR TROUBLESHOOTING
            # for line in cme_events:
            #     print(f"this is from file: {line}")
    except FileNotFoundError:
        with open("CME_events.txt", 'w') as my_file:
            my_file.write("")
            cme_events = []

    with open("CME_events.txt",'w') as my_file:
        for item in cme_list:
            if item in cme_events:
                continue
            my_file.write(f"{item}\n")
            # my_file.write('%s\n' % item)
            print(item)
#--------------------------------------------------------------------------------------------------------------


#----------------------MESSAGEBOX FUNCTION FOR CME LIST DISPLAY-----------------------------

def display_cme_list():
    cme_list = generate_cme_list()
    my_string = ""
    for item in cme_list:
        my_string += f"{item}\n\n"
    messagebox.showinfo(message=my_string)




#---------------------------------------CREATE GUI-------------------------------------------------------------

window = Tk()
window.title("NASA CME UPDATES")
window.config(padx=20, pady=20)

cme_image = PhotoImage(file="cme_image.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100,100,image=cme_image)
canvas.grid(columnspan=2,row=1)

title = Label(text = "CME Updates", font = ("Courier",40,"bold"))
title.grid(columnspan=2,row=0)

generate_file = Button(text="Generate text file",command = update_text_file)
generate_file.grid(columnspan=2,row=2,sticky="w")

display_list_button = Button(text = "Display CMEs",command = display_cme_list)
display_list_button.grid(column=1,row=2,sticky="e")


window.mainloop()


