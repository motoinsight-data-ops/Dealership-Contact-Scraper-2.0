from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers import *
import pandas as pd
import os
import csv

CWD = os.path.dirname(os.path.realpath(__file__))


"""
------------------------------------------------------------------------
Gets dealership staff contact info based on the provider. scrapers.py contains
a variety of different scrapers for the most popular dealership site providers.

Outputs contact information of staff in list of JSON (Python Dictionairy)
in the form of a string. 
------------------------------------------------------------------------
Author: Andrei Secara & Naftal Kerecha - Data & Automation
Updated: June 17, 2021
------------------------------------------------------------------------
Notes:
- To use this program, you must navigate to ./src and type in python run.py

- All excel file inputs should be placed in ./spreadsheets

- Excel file should containg 'URL', and completed 'Site Provider' column (can be completed by running the Dealership Provider Scraper also on the Github)

- After that, you must pick an EXCEL file (.xlsx) to input from the list that appears
- (Please type the file name accurately including the extension)

- Let it run. It will take a while depending on how many sites you are checking,
but it is tested to avoid hanging / freezing. 

* In the case of a crash / unexpected faliure, all data gets saved to the respective spreadsheet name in the ./save folder


---
Output meanings in the 'Staff Contact' column:

[{'name': ‘Germaine Russel’, 'position': ‘Sales Consultant’, 'email': ‘grussell@youngermitsubishi.com’, 'phone': ‘240-527-2357’}] - SUCCESSFUL SCRAPE

FALSE - Could not find staff contact on the page. For good measure, check out the page yourself and confirm there is indeed no staff contact. From tests is right about 85% of the time.

TRUE- Staff contact info found but the site provider does not have a dedicated scraper. Must scrape manually.

CAPTCHA ERROR - Could not get into the site because of a captcha blocking the bot.



---

------------------------------------------------------------------------
"""

# For removing bugs. Found solution at https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')



class ContactScraper:
    def setup_method(self):
        print("Launching driver...")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Temporary CSV save file location for main file to append to while running through rows
        self.tempSaveFileLocation = CWD + "/../save/"

        self.vars = {}
        
        # Placeholder for dataframe object
        self.df = None
        return


    def teardown_method(self):
        print("Shutting down driver...")
        self.driver.quit()
        return

    
    def readFromExcel(self):
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir(CWD + "/../spreadsheets"))

        excel_file_name = input("File name: ")
        self.excel_file_path = CWD + "/../spreadsheets/" + excel_file_name
        self.output_file_path = CWD + "/../spreadsheets/" + excel_file_name[0:-5] + " output.xlsx"

        self.df = pd.read_excel(self.excel_file_path)

        # Update temporary save file to have the same name as the input excel file
        self.tempSaveFileLocation += excel_file_name[0:-5] + '.csv'

        print("File read into object dataframe from: " + self.excel_file_path)
        print()
        return

    def saveRow(self, url, staffPage, salesContactNumber, staffContactList):
        try:
            with open(self.tempSaveFileLocation, 'a+') as saveFile:
                output_writer = csv.writer(saveFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                # Append one line containing the following information
                output_writer.writerow([url, staffPage, salesContactNumber, staffContactList])
        except:
            return
        return


    def contactScraper(self):
        partial_scrape = "Scrape" in self.df.columns
        staffPageList = []
        salesContactList = []
        staffContactList = []
        cur = 0
        numRows = len(self.df.index)
        for index, row in self.df.iterrows():
            cur += 1

            if partial_scrape and row['Scrape'] is False:
                # print("Scrape option is set to FALSE, skipping dealership.")
                staffPageList.append("SKIPPED")
                salesContactList.append("SKIPPED")
                staffContactList.append("SKIPPED")
                continue
            else:
                print()
                print("Page: ", cur, " / ", numRows)
                print("{}\n{}".format(row['Name'], row['URL']))

            try:
                url = row['URL'].lower()
                row['URL'] = url
            except:
                # In case URL is messed up
                result['Sales'] = 'Check Manually.'
                result['Staff Page'] = 'Check Manually.'
                result['Staff Contact'] = 'Check Manually'
                self.saveRow(url, result['Staff Page'], result['Sales'], result['Staff Contact'])
                staffPageList.append(result['Staff Page'])
                salesContactList.append(result['Sales'])
                staffContactList.append(result['Staff Contact'])
                cur += 1
                continue


            # provider = str(row['Site Provider']).lower()
            # print("Provider: "+ provider)
            # if provider == 'dealer.com':
            #     result = scraper_dealerDotCom(self.driver, url)
            
            # elif provider == 'dealerinspire':
            #     result = scraper_dealerInspire(self.driver, url)
            
            # elif provider == 'dealerfire':
            #     result = scraper_dealerFire(self.driver, url)

            # elif provider == 'dealeron':
            #     result = scraper_dealerOn(self.driver, url)
            
            # elif provider == 'dealereprocess':
            #     result = scraper_dealerEprocess(self.driver, url)
            
            # If none of the previous site providers, a general scraper will be used to check if there is a staff page on the sitemap or not. 
            # Knowing if a page has a staff page or not will be useful when scraping manually later as we will know whether its worth it to look for one or not.
            # else:
            #     result = scraper_Common(self.driver, url)
            result = scraper_Common(self.driver, url)
            # result = scraper_Common(self.driver, url)
            
            # if provider == 'dealervenom':
            #     # result = {'Staff Page': True/False, 'Sales': 519-123-1234, 'Staff Contact': True/False}
            #     result['Staff Page'] = 'Check Manually.'
            #     result['Staff Contact'] = 'Check Manually'

            # Format of result JSON / Python Dictionary: result = {Staff Page: True/False, Sales: 519-123-1234, Staff Contact: True/False}
            
            

            if result['Staff Page'] == None and result['Sales'] == None and result['Staff Contact'] == None:
                # This happens when a captcha is found
                result['Staff Page'] = 'CAPTCHA ERROR'
                result['Sales'] = 'CAPTCHA ERROR'
                result['Staff Contact'] = 'CAPTCHA ERROR'
                
            # print(result)
            # After result is generated, save the row to a temporary save file in case of catastrophic faliure (program crashes midway through)
            self.saveRow(url, result['Staff Page'], result['Sales'], result['Staff Contact'])

            # Append to rows that will later be added to the dataframe
            staffPageList.append(result['Staff Page'])
            salesContactList.append(result['Sales'])
            staffContactList.append(result['Staff Contact'])


        # Add new completed columns to dataframe
        self.df['Staff Page'] = staffPageList
        self.df['Sales Number'] = salesContactList
        self.df['Staff Contact List'] = staffContactList
        return
    
    def saveToExcel(self):
        print("Saving to excel file: " + self.output_file_path)
        writer = pd.ExcelWriter(self.output_file_path)
        self.df.to_excel(writer)
        writer.save()
        return