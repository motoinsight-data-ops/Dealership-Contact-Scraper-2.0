"""
------------------------------------------------------------------------
Takes the files from other scripts and merges them with the preferred
formatting for dealer prospects as of the date of creating this script.
------------------------------------------------------------------------
Authors: Kelvin Kellner & Jiten Aylani
Updated: 2021-10-06
------------------------------------------------------------------------
Note: The script takes care of 90% of the work, look over the new_format
file and correct any mistakes, then save finished copy into new_final.
------------------------------------------------------------------------
"""


import ast
import pandas as pd
from copy import deepcopy
import os
import re
import json
from types import SimpleNamespace
pd.options.mode.chained_assignment = None  # default='warn'


OUTPUTFILEDIR = '/../new_format/'
BRANDNAME = input("Please enter the Brand name: ")

CWD = os.path.dirname(os.path.realpath(__file__))

def readFromExcel():
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir(CWD + "/../cleaned"))

        excel_file_name = input("File name: ")
        excel_file_path = CWD + "/../cleaned/" + excel_file_name

        df = pd.read_excel(excel_file_path)

        print("File read into object dataframe from: " + excel_file_path)
        print()
        return df

def pre_process(df):
        n = len(df['Name'])
        # df.drop('Staff Contact List', inplace=True)
        df['Employee Name'] = [None]*n
        df['Position'] = [None]*n
        df['Email'] = [None]*n
        df['Phone'] = [None]*n
        return df

def split_employees(df_main):
        column_headers = ["Store No.", "Name", "Brand", "Autogroup", "# of Dealers", "Address", "City", "State", "Zip Code", "Phone Number", "Fax", "URL", "Sales Number", "Employee", "Position", "Email", "Number"]
        new_df = pd.DataFrame(columns=column_headers)
        error_msg = None
        # for each dealer
        for i in range(len(df_main['Name'])):
                if str(df_main['Staff Contact List'][i]) not in ["NaN", "nan", "NO CONTACTS", "COULD NOT SCRAPE", "ALREADY PRESENT SOMEWHERE ELSE"] and not isinstance(df_main['Staff Contact List'][i], bool):
                        try:
                                employees = ast.literal_eval(df_main['Staff Contact List'][i])
                        except:
                                employees = []
                                error_msg = '(PROBLEM WITH STAFF LIST - INPUT MANUALLY)'
                else:
                        employees = []
                        error_msg = 'NO STAFF LIST FOUND'
                if str(df_main['Name'][i]) != 'nan':
                        print(df_main['Name'][i])
                        if employees != []:
                                # for each employee
                                for employee in employees:
                                        if employee["name"]:
                                                # handle special cases of cleaning
                                                for key in ["name", "position", "email", "phone"]:
                                                        if employee[key]:
                                                                if "&amp;" in employee[key]:
                                                                        employee[key] = employee[key].replace("&amp;", "&")
                                                                if "<Font" in employee[key] or "<font" in employee[key]:
                                                                        employee[key] = re.sub(r'<[fF]ont[\s\d\w\S\W\D]*?>', "", employee[key])
                                                                for s in ["<BR><BR>", "<br><br>", "</b>", "<b>", "</br>", "&nbsp;", "</font>", "<strong>", "</strong>", "\\xa0", "rep_email="]:
                                                                        if s in employee[key]:
                                                                                employee[key] = employee[key].replace(s, "")
                                                                if "window.datalayer" in employee[key]:
                                                                        employee["name"] = "PROBLEM WITH EMPLOYEE INFO - INPUT MANUALLY"
                                                                        employee["position"] = None
                                                                        employee["email"] = None
                                                                        employee["phone"] = None
                                                for s in [", <br>", ", <BR>", " <BR> ", " <br> ", " <br>", "<br>", "<BR>"]:
                                                        if employee["position"] and s in employee["position"]:
                                                                employee["name"] = employee["position"]
                                                        if s in employee["name"]:
                                                                temp = employee["name"].split(s)
                                                                if employee["position"]:
                                                                        if len(temp[0].split(" ")) <= 1:
                                                                                if len(temp) <= 2:
                                                                                        employee["name"] = employee["name"].replace(s, " ")
                                                                                else:
                                                                                        employee["name"] = "{} {}".format(temp[0], temp[1])
                                                                                        employee["position"] = temp[2:].join(" ")
                                                                else:
                                                                        employee["name"] = temp[0]
                                                                        employee["position"] = temp[1]
                                                if employee["phone"] and "<br>" in employee["phone"]:
                                                        employee["phone"] = employee["phone"].replace("<br>", ", ")
                                                for key in ["name", "position", "email", "phone"]:
                                                        if employee[key]:
                                                                employee[key] = employee[key].strip()
                                                                while "  " in employee[key]:
                                                                        employee[key] = employee[key].replace("  "," ")

                                                # fill data as normal
                                                new_entry = {}
                                                for key in column_headers:
                                                        new_entry[key] = None
                                                new_entry["Zip Code"] = df_main["Zip_Code"][i]
                                                new_entry["Phone Number"] = df_main["Phone Number"][i]
                                                new_entry["Brand"] = BRANDNAME
                                                for s in ["Store No.", "Name", "Address", "City", "State", "URL", "Sales Number"]:
                                                        new_entry[s] = df_main[s][i]
                                                new_entry["Employee"] = employee["name"]
                                                new_entry["Position"] = employee["position"]
                                                new_entry["Email"] = employee["email"]
                                                new_entry["Number"] = employee["phone"]
                                                new_df = new_df.append(new_entry, ignore_index=True)
                        if employees == []:
                                # if no employees are listed
                                new_entry = {}
                                for key in column_headers:
                                        new_entry[key] = None
                                new_entry["Zip Code"] = df_main["Zip_Code"][i]
                                new_entry["Phone Number"] = df_main["Phone Number"][i]
                                new_entry["Brand"] = BRANDNAME
                                for s in ["Store No.", "Name", "Address", "City", "State", "URL", "Sales Number"]:
                                        new_entry[s] = df_main[s][i]
                                if error_msg == "NO STAFF LIST FOUND":
                                        new_entry["Employee"] = "Sales Team"
                                        new_entry["Position"] = "(No Staff List Found)"
                                        new_entry["Number"] = df_main["Sales Number"][i]
                                else:
                                        new_entry["Position"] = error_msg
                                new_df = new_df.append(new_entry, ignore_index=True)
        print(new_df)
        return new_df

def saveToExcel(df):
        # FILENAME = input("Desired file name (eg. [Brand]_USA_new_format.xlsx): ")
        FILENAME = "{}_USA_new_format.xlsx".format(BRANDNAME)
        print("Saving to excel file: " + CWD + OUTPUTFILEDIR + FILENAME)
        writer = pd.ExcelWriter(CWD + OUTPUTFILEDIR + FILENAME)
        df.to_excel(writer, index=False)
        writer.save()
        return

df_main = readFromExcel()

df_main = pre_process(df_main)

df_new_format = split_employees(df_main)

saveToExcel(df_new_format)

print("Finished")