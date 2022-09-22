import requests
from prettytable import PrettyTable


CME_ENDPOINT = "https://api.nasa.gov/DONKI/CME?api_key=DEMO_KEY"
PIC_OF_DAY_ENDPOINT = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
NEO_ENPOINT = "https://api.nasa.gov/neo/rest/v1/feed?api_key=DEMO_KEY"
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
    i = 1
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
                my_table.add_row(i,name,clean_time_date,clean_time)
    print("all done creating new CME list")

    return new_list

#-------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------

def generate_neo_list():
    data = retrieve_data(NEO_ENPOINT)
    neo_table = PrettyTable()
    neo_table.field_names = ["I.D.","Approach Date","Max Diameter (meters)","Miss Distance (miles)","Relative Velocity (mph)"]

    new_list = list(data["near_earth_objects"].items())
    i = 0
    for k,v in new_list:
        
        for item in v:
            # print(item["is_potentially_hazardous_asteroid"])
            if item["is_potentially_hazardous_asteroid"] == True:
                id = (item["id"])
                i += 1
                approach_date = item["close_approach_data"][0]["close_approach_date"]
                diameter = item["estimated_diameter"]["meters"]["estimated_diameter_max"]
                miss = item["close_approach_data"][0]["miss_distance"]["miles"]
                velocity = item["close_approach_data"][0]["relative_velocity"]["miles_per_hour"]
               
                # print(f"id: {id} will approach on {approach_date}")
                neo_table.add_row([id,approach_date,int(diameter),int(float(miss)),int(float(velocity))])
                
    print(neo_table) 
beans = input("This program is for checking out Near Earth Objects (NEOs), meteorites and occasionally comets that cross Earth's orbit. \n\nPress 'y' and hit 'enter' to create a list of near earth objects that are approaching in the next 7 days and have been labeled 'hazardous.'  \n\nPress anything else then 'enter' to abort without making a NEO list.\n\nI couldn't get Tkinter working, so you might have to expand the window since the GUI is just PrettyTables.\nYou get what you get and you don't throw a fit.")

if beans == 'y':
    generate_neo_list()
else:
    exit()