"""
------------------------------------------------------------------------
Very niche tool used to convert manually created staff contact spreadsheets into 
a list of JSON string format.

To use, populate a spreadsheet with dealership contact info in the following format:

Name        Title           Email           Phone
John F.     President       jfk@gmail.com   123-456-7890
...         ...             ...             ...
...         ...             ...             ...

Then, run this file and select your spreadsheet as an input.
** Make sure to put that spreadsheet in ../Manual Staff Contacts beforehand

It will then output a string in the correct format to input into the appropriate column
of the OEM input sheet.
------------------------------------------------------------------------
Author: Andrei Secara - Data & Automation
Updated: 2020-12-14
------------------------------------------------------------------------
Notes:

This will only be used for the minority of websites that the scrapers miss.
------------------------------------------------------------------------
"""


import pandas as pd
from copy import deepcopy
import os

def readFromExcel():
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir("../Manual Staff Contacts"))

        excel_file_name = input("File name: ")
        excel_file_path = "../Manual Staff Contacts/" + excel_file_name

        df = pd.read_excel(excel_file_path)

        

        print("File read into object dataframe from: " + excel_file_path)
        print()
        return df

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

df = readFromExcel()
convertToJSONString(df)