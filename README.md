# Dealership Contact Scraper 2.0

Visits a list dealership websites and attempts to scrapes contact information from Staff/Team pages.

## How to Use

1. Place the input .xlsx file containing dealership URLs and other info into /spreadsheets.
2. Navigate to /src and run "run.py", follow instructions to select the appropriate file and begin scraping. The script takes about a minute per dealership (may vary), so prepare device usage accordingly, and take precautions to prevent overheating or crashing if possible/necessary.
3. If the script does crash for whatever reason, progress is dumped into a file in /save with the same name as the input file, you can add an additional column titled "Scrape" to the input file with a value of "TRUE" or "FALSE" for each dealership as to whether or not you want the script to scrape that dealership's website. Results from multiple runs can be combined manually if needed.
4. When your output file is prepared, navigate to /tools and run "clean_data.py", this script will do basic cleaning of the ouptut file from /spreadsheets and export to /cleaned.
5. Next, still in /tools, run "new_format.py" and follow instructions to create the final prospecting list using the file in /cleaned and exporting to /new_format.
6. Look over the file in /new_format, if there are any errors please fix them in the file in /cleaned and restart from Step 5. The "manual_staff_list.py" file can help create staff lists if any dealerships are incorrectly missing data. When the file in /new_format looks perfect at last, copy it into /new_format_final and you are done!

## Descriptions of Files and Folders

### /src

src: contains main python files used to scrape content from dealership websites

- src/run.py: the launcher used to call the web scrapers and produce output files

### /tools

tools: contains python files which provide tools to clean output files, help create input files, and more

- tools/clean_data.py: performs basic cleaning of the output file in /spreadsheets and exports to /cleaned

- tools/manual_staff_list.py: can be used to convert a manually entered .xlsx staff list to a JSON-style python object as seen in /cleaned files

- tools/new_format.py: takes a file from /cleaned and does the final formatting and exports to /new-format

### Other folders

- /spreadsheets: place input files here, and scraper will create output files here aswell

- /cleaned: contians cleaned but not-yet formatted output files

- /new-format: contains cleaned and formatted output files

- /new-format-final: contains cleaned and formatted output files which have been checked and confirmed to be correct, ready to be sent off

- /save: the scraper dumps its progress to files in this folder in case of a crash or error while running

- /manual_staff_contacts: used as the input folder for "manual_staff_list.py" tool

## Authors

- [Andrei Secara](https://github.com/AndreiSec)
- Naftal Kerecha
- [Kelvin Kellner](https://github.com/kelvinkellner)
- [Jiten Aylani](https://github.com/aylanij)
