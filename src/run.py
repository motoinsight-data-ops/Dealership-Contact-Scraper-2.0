"""
Refer to domainCheck.py for documentation.

This is just the execution file.
    
"""


from main import ContactScraper


cs = ContactScraper()

# Set up driver and placeholder variables
cs.setup_method()

# Read data from excel into dc
cs.readFromExcel()

# Scrape contact info from URL list generated in readFromExcel()
cs.contactScraper()

# Save updated dataframe containing site providers to excel
# cs.saveToExcel()

# Quit driver and exit program
cs.teardown_method()