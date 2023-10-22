from datetime import datetime
import json

# This program provides a .json of every functioning Starlink satellite's NORAD ID 
# grouped by their launch dates. It also has the functionality to provide all of 
# the table data for each satellite (although it is not included in the final .json).

# The data is taken from the <tbody> portion on the "Starlink Satellites" website
# from NORAD which displays the name, NORAD ID, Int'l Code, and Launch Date
# for every functioning Starlink satellite.

# Data from NORAD as of 10/22/2023

# Data wanted for each Starlink sattelite:
#     1. name
#     2. NORAD id
#     3. Int'l Code
#     4. Launch date

files = ['test_data.txt', 'original_data.txt']

f = open(files[1], 'r')
content = f.readlines()
content = content[1:-1] # remove first and last lines container

step = 20 # every 20 lines of content

composite_list = [content[x:x+step] for x in range(0, len(content), step)]

data = {}
dates = set()
for i in range(len(composite_list)):
    group = composite_list[i]
    for j in range(len(group)):
        if "STARLINK" in group[j]: # name line
            name = group[j][37:-5]
            data[name] = {"name": name}
        elif j == 5: # NORAD ID line
            id = group[j][-11: -6]
            data[id] = data.pop(name)
            data[id]["id"] = id
        elif j == 6: # Int'l Code line
            intl_code = group[j][-15:-6]
            data[id]["code"] = intl_code
        elif j == 8: # Launch date line
            date = group[j].split('">',1)[1][:-5]

            date_format = '%B %d, %Y'
            date_obj = datetime.strptime(date, date_format)
            date_obj = date_obj.date()
            date = date_obj.strftime("%Y.%m.%d")

            data[id]["date"] = date
            dates.add(date_obj)

# convert datetime set to sorted list of dates
def sortDates(date_set: set) -> list:
    dates = list(date_set)
    dates = sorted(dates)
    sorted_dates = []
    for date in dates:
        sorted_dates.append(date.strftime("%Y.%m.%d"))

    return sorted_dates

# get new dict of {launch_date0: [NORAD_ID0, NORAD_ID1, NORAD_ID2, ...], ...}
# given data dictionary and list of sorted/formated dates
# data dict date strings should match dates list strings
def groupByDate(data: dict, dates: list):
    date_dict = {}
    for date in dates:
        date_dict[date] = []
        for sat in data: # sat is each key of data dict
            if data[sat]["date"] == date:
                date_dict[date].append(data[sat]["id"])

    return date_dict

# # Get date/time
# now = datetime.now()
# dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
# print(dt_string)


if __name__ == "__main__":
    date_dict = groupByDate(data, sortDates(dates))
    # print(date_dict)

    # # Get list of NORAD IDs
    # id_list = list(data.keys())
    # print(id_list)

    # Comment this block if you have already made the .json file
    json_obj = json.dumps(date_dict, indent=4)
    with open("sat_data.json", "w") as outfile:
        json.dump(date_dict, outfile)