"""
------------------------------------------------------------------------
Very niche tool used to convert manually created staff contact spreadsheets into 
a list of JSON string format.

To use, populate a spreadsheet with contact info in the following format:

Name        Title           Email           Phone
John F.     President       jfk@gmail.com   123-456-7890
...         ...             ...             ...
...         ...             ...             ...

(for single dealership - convertToJSONString)

Or in following format:

Store No.   Dealership      Name            Title           Email           Phone
05125       President Volvo John F.         President       jfk@gmail.com   123-456-7890
...         ...             ...             ...             ...             ...
...         ...             ...             ...             ...             ...

(for multiple dealerships - convertToJSONStrings)

Then, run this file and select your spreadsheet as an input.
** Make sure to put that spreadsheet in /../manuals_staff_contacts beforehand

It will then output (or create a txt file) with string(s) in the correct format
to input into the appropriate column(s) of the OEM input sheet.
------------------------------------------------------------------------
Authors:
    Andrei Secara - Data & Automation
    Kelvin Kellner - Data & Automation
Updated: 2021-10-26
------------------------------------------------------------------------
Notes:

This will only be used for the minority of websites that the scrapers miss.
------------------------------------------------------------------------
"""


import pandas as pd
from copy import deepcopy
import os

CWD = os.path.dirname(os.path.realpath(__file__))

FOLDER = "/../manual_staff_contacts"

def readFromExcel():
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir(CWD + FOLDER))

        excel_file_name = input("File name: ")
        excel_file_path = CWD + FOLDER + excel_file_name

        df = pd.read_excel(excel_file_path)

        output_file_path = CWD + FOLDER + excel_file_name[:-5] + " output.txt"

        print("File read into object dataframe from: " + excel_file_path)
        print()
        return df, output_file_path

def convertToJSONString(df):
    l = []
    for index, row in df.iterrows():
        tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
        name = row['Name']
        title = row['Title']
        email = str(row['Email'])
        phone = str(row['Phone'])
        
        tempEmployeeContact['name'] = name
        tempEmployeeContact['position'] = title
        if email is not None:
            tempEmployeeContact['email'] = email.replace("mailto:", "").replace('\n', '')
        
        if phone is not None:
            tempEmployeeContact['phone'] = phone.replace("tel:", '')
        
        l.append(deepcopy(tempEmployeeContact))
    
    print("List")
    print(l)

def convertToJSONStrings(df, output_file_name):
    key = 'Store No.' if 'Store No.' in df.columns else 'Dealership' if 'Dealership' in df.columns else None
    if key:
        stores = {}

        for index, row in df.iterrows():
            store = row[key]

            tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
            name = row['Name']
            title = row['Title']
            email = str(row['Email'])
            phone = str(row['Phone'])
            
            tempEmployeeContact['name'] = name
            tempEmployeeContact['position'] = title
            if email is not None and email != 'nan':
                tempEmployeeContact['email'] = email.replace("mailto:", "").replace('\n', '')
            
            if phone is not None and phone != 'nan':
                tempEmployeeContact['phone'] = phone.replace("tel:", '')
            
            if store in stores.keys():
                stores[store].append(deepcopy(tempEmployeeContact))
            else:
                stores[store] = [deepcopy(tempEmployeeContact)]

        f = open(output_file_name, "w")
        for key in stores.keys():
            print("\n-----\n{}\n{}".format(key, stores[key]))
            f.write("\n-----\n" + key + "\n" + str(stores[key]) + "\n")
        f.close()
        print("Finished writing to " + output_file_name)


    else:
        print("Could not create JSON lists for multiple dealerships,\ncheck function called for plural or singular, or include Store No. or Dealership in file.")

df, output_file_name = readFromExcel()
convertToJSONString(df)
# stores = convertToJSONStrings(df, output_file_name)
