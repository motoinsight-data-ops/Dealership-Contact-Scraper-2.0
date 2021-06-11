# Dealership Contact Scraper 2.0
 Gathers (if available) individual staff contact information from a list of dealership URLs.

## Description of folders:

cleaned: Contains Cleaned .xlsx files (files will be outputted here after running clean_data in tools)

final: Contains *final* cleaned and formatted .xlsx files. 

formatted_csv: Contains the csv output of the format_output tool that you will have to copy the data from and paste into the respective final .xlsx file.

save: Contains .csv temporary save files (these are populated everytime the scraper goes through each row, and is there in case the scrapers unexpectedly crashes and loses all its progress.)

spreadsheets: Contains input spreadsheets for the scraper functions.

src: Contains main scraper code

tools: Contains a variety of tools to clean and format the data. Documentation on each can be found in the file.