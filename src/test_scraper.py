from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapers import *
import pandas as pd
import os
import csv

'''
JUST A FILE TO TEST INDIVIDUAL SCRAPERS. 
WAS USED IN DEVELOPMENT, YOU CAN IGNORE UNLESS YOU WANT TO TEST A SCRAPER INDIVIDUALLY.

'''


URL1 = 'https://www.capemitsu.com' # Dealer dot com

URL2 = 'https://www.schaumburgmitsubishi.com' # Dealer e process

URL3 = 'https://www.mitsubishistore.com' # DealerOn

URL4 = 'https://www.jeffschmittmitsubishi.com' # Dealer inspire

URL5 = 'https://www.superiormitsubishi.com' # Weird number

URL6 = 'https://www.mitsubishiofoxford.com' # didn't find staff page

URL7 = 'https://www.stuckeymitsubishi.com' # didn't find email on staff page?

URL8 = 'https://www.broncomotorsmitsubishi.com' # no emails just numbers on staff page

URL9 = 'https://www.valleyimportsmitsubishi.com' # dealer dot com test 2

URL10 = 'https://www.stuckeymitsubishi.com' # dealer dot com test 3

URL11 = 'https://www.bakersfieldmitsubishi.com' # Null error finding site map and staff page?

DEALERINSPIRESITES = ['https://www.universitymitsubishi.com', 'https://www.mitsu44.com', 'https://www.joemachensmitsubishi.com']

DEALERONSITES = ['https://www.andymohravonnissan.com', 'https://www.andymohr-nissan.com', 'https://www.antwerpennissanowingsmills.com', 'https://www.antwerpensecuritynissan.com', 'https://www.bayounissan.com', 'https://www.becknissan.com']


DEALERFIRESITES = ['https://www.bouchernissangreenfield.com', 'https://www.coastnissan.com', 'https://www.buycolonialnissan.com']


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

urlList = [URL1, URL2, URL3, URL4]

# result = scraper_Common(driver, 'https://www.harrismitsubishi.com')
url = 'https://www.adanissan.com/MeetOurDepartments'
# result = scraper_dealerOn(driver, 'https://www.andymohravonnissan.com')
driver.get(url)
result = get_staff_contact_common(driver, url)
print("\nResult:")
print(result)



# for url in DEALERINSPIRESITES:
#     print("Processing url: " + url)
#     result = scraper_dealerInspire(driver, url)
#     print("\nResult:")
#     print(result)


driver.quit()