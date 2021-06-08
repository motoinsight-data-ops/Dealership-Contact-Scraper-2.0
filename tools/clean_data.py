"""
------------------------------------------------------------------------
Removes junk content from the scraped sheets.
------------------------------------------------------------------------
Author: Andrei Secara - Data & Automation
Updated: 2020-12-14
------------------------------------------------------------------------
Notes:

A problem we found with the scrapers was inconsistency with extracting 
emails and phone numbers from the HTML content, so this takes it one more
step and removes and HTML junk content from each row of the scraped sheet.
------------------------------------------------------------------------
"""


import pandas as pd
from copy import deepcopy
import os
import re
import json

# The phone pattern that regular expression will use to match on the page text
PHONEPATTERN = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}?')

# Pattern to check for emails
EMAILPATTERN = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")

OUTPUTFILEDIR = '../cleaned/'

def readFromExcel():
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir("../spreadsheets"))

        excel_file_name = input("File name: ")
        excel_file_path = "../spreadsheets/" + excel_file_name

        df = pd.read_excel(excel_file_path)

        global OUTPUTFILEDIR 
        OUTPUTFILEDIR += excel_file_name

        print("File read into object dataframe from: " + excel_file_path)
        print()
        return df

def cleanData(df):
        cleaned_list = []
        for index, row in df.iterrows():
                outputList = []
                
                
                try:
                        row['Staff Contact List'] = row['Staff Contact List'].replace('\n', '').replace('‘', '\'').replace('’', '\'')
                except:
                        # Row is not a string, but instead it is a boolean
                        cleaned_list.append(row['Staff Contact List'])
                        continue
                try:
                        inputList = eval(row['Staff Contact List'])
                except:
                        # Row is not a list of python dict
                        cleaned_list.append(row['Staff Contact List'])
                        continue
                # print('Length of inputlist: ', len(inputList))
                for employee in inputList:
                        tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}

                        
                        try:
                                if employee['email'] == '''\n<a href="mailto:"></a>\n''':
                                        employee['email'] = ''
                                # print(employee['email'])
                                tempEmail = re.search(EMAILPATTERN, employee['email'])

                                if tempEmail is not None:
                                        employee['email'] = tempEmail.lower().group(0)
                                else:
                                        employee['email'] = ''
                                
                                # print(employee['email'])
                                employee['email'] = employee['email'].replace('\n', '')
                                # print('2 ', employee['email'])
                        except Exception as e:
                                employee['email'] = employee['email']
                        
                # print(row['Staff Contact List'])
                cleaned_list.append(str(inputList))
                # print('2', row['Staff Contact List'])
        df['Staff Contact List'] = cleaned_list
        return df


def saveToExcel(df):
        print("Saving to excel file: " + OUTPUTFILEDIR)
        writer = pd.ExcelWriter(OUTPUTFILEDIR)
        df.to_excel(writer)
        writer.save()
        return

df = readFromExcel()
df = cleanData(df)

saveToExcel(df)