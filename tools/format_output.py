import pandas as pd
from copy import deepcopy
import os
import re
import csv

excel_file = ''

def readFromExcel():
    print("Type in the name of the spreadsheet you want to domain check: \n")

    print(os.listdir("../spreadsheets"))

    excel_file_name = input("File name: ")
    excel_file_path = "../spreadsheets/" + excel_file_name

    global excel_file
    excel_file = excel_file_name

    df = pd.read_excel(excel_file_path)

    

    print("File read into object dataframe from: " + excel_file_path)
    print()
    return df


def formatData(df):
    formatted_list = []
    for index, row in df.iterrows():
        outputList = []
        
        
        try:
                row['Staff Contact List'] = row['Staff Contact List'].replace('\n', '').replace('‘', '\'').replace('’', '\'')
        except:
                # Row is not a string, but instead it is a boolean
                formatted_list.append(row['Staff Contact List'])
                continue
        try:
                inputList = eval(row['Staff Contact List'])
        except:
                # Row is not a list of python dict
                formatted_list.append(row['Staff Contact List'])
                continue
        # print('Length of inputlist: ', len(inputList))
        for employee in inputList:
            temprow = []
            # print(employee)
            for key, value in employee.items():
                temprow.append(value)
            formatted_list.append(deepcopy(temprow))

                    
            
    
    return formatted_list



def output_to_csv(employee_contact_list_formatted):
    d = '../formatted_csv/' + excel_file
    d.replace('.xlsx', '.csv')
    # Open csv file or create one if not there. Also overwrites any existing files with the same name.
    print()
    print("Outputting data to file: " + d)
    print()
    with open(d, mode='w+') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        

        for employee_row in employee_contact_list_formatted:
            output_writer.writerow(employee_row)
    
    print("Finished. CLosing Driver.")


df = readFromExcel()
l = formatData(df)
for i in l:
    print(i)
output_to_csv(l)