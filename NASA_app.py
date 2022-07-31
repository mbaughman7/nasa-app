import requests
from datetime import datetime
from tkinter import *
from tkinter import messagebox


CME_ENDPOINT = "https://api.nasa.gov/DONKI/CME?api_key=DEMO_KEY"
PIC_OF_DAY_ENDPOINT = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
#=========================CME_UPDATER=======================================================

#-------------------------DATA RETRIEVAL FROM API--------------------------------------------
def retrieve_data(api_url):
    response = requests.get(api_url)
    code = response.status_code
    print(f"GET request sent.  status code of {code} returned")

    response.raise_for_status()
    raw_data = response.json()
    return raw_data
#--------------------------------------------------------------------------------------------



#-------------------------GENERATE CLEAN LIST OF CMEs THAT WILL HIT EARTH-----------------------------------

def generate_cme_list():

    data = retrieve_data(CME_ENDPOINT)
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
                entry = f"CME identified as {name} will impact earth on {clean_time_date} at approx {clean_time} UTC."
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
            print("about to print contents of file...")
            print(cme_events)
            ### FOR TROUBLESHOOTING
            # for line in cme_events:
            #     print(f"this is from file: {line}")
    except FileNotFoundError:
        print("file not found.  generating file...")
        with open("CME_events.txt", 'w') as my_file:
            my_file.write("")
            cme_events = []

    with open("CME_events.txt",'a') as my_file:
        for item in cme_list:
            list_item = item + '\n'
            if list_item in cme_events:
                print("skipping")
                continue
            else:
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
#=====================================END OF CME UPDATER==============================================



#---------------------MESSAGEBOX FUNCTION FOR DISPLAY DAILY PIC-------------------------------
def display_link():
    data = retrieve_data(PIC_OF_DAY_ENDPOINT)
    my_link=data["url"]
    print(my_link)
    messagebox.showinfo(message=my_link)




#---------------------------------------CREATE GUI-------------------------------------------------------------

window = Tk()
window.title("NASA UPDATES")
window.config(padx=20, pady=20)


#------------------------------cme stuff---------------------------------------------------
cme_image = PhotoImage(file="cme_image.png")
sun_canvas = Canvas(width=100, height=100)
sun_canvas.create_image(50,50,image=cme_image)
sun_canvas.grid(column=0,row=1,sticky="w")

title = Label(text = "NASA STUFF", font = ("Courier",40,"bold"))
title.grid(columnspan=2,row=0)

display_list_button = Button(text = "Display CMEs",command = display_cme_list,width=13)
display_list_button.grid(column=0,row=2,sticky="w")

generate_file = Button(text="Generate text file",command = update_text_file)
generate_file.grid(column=0,row=3,sticky="w")
#--------------------------------------------------------------------------------------------

#------------------------------daily pic-----------------------------------------------------
pic_canvas = Canvas(width=100,height=100,background="green")
pic_canvas.grid(column=1,row=1,sticky="e")

display_pic_link = Button(text = "Display link",command = display_link,width=13)
display_pic_link.grid(column=1,row=2,sticky="e")




window.mainloop()
