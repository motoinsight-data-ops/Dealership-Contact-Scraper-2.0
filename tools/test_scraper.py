from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapers import *
import time

'''

HERE FOR TESTING, YOU CAN IGNORE

'''


CARSGUAM = 'https://www.carsguam.com/staff/'

VOLVOWHITEPLAINS = 'https://www.volvocarswhiteplains.com/meet-our-team.htm'

KOONSVOLVO = 'https://www.koonsvolvocarswhitemarsh.com/koons-staff.htm'

CHERRYHILLVOLVO = 'https://www.cherryhillvolvocars.com/staff-demo.htm'

BERWYNVOLVO = 'https://www.berwynvolvo.com/meet-our-staff.htm'

MIDLOTHIANVOLVO = 'https://www.volvocarsmidlothian.com/dealership/staff.htm'

FINDLAYVOLVO = 'https://www.findlayvolvocarslv.com/dealership/staff.htm'

NORTHFIELDVOLVO = 'https://www.volvonorthfield.com/dealership/staff.htm'

VOLVODANBURY = 'https://www.volvocarsdanbury.com/meet-our-team.htm'

PAULMOAKVOLVO = 'https://www.paulmoakvolvocars.com/staff.htm'

MAPLEHILLVOLVO  = 'https://www.maplehillvolvo.com/dealership/staff.htm'

COURTESYVOLVOCARS = 'https://www.courtesyvolvocarsofscottsdale.com/dealership/staff.htm'

NORTHMIAMIVOLVOCARS = 'https://www.volvocarsnorthmiami.com/dealership/staff.htm'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://www.claycooleymitsubishiofarlington.com/about-us/mitsubishi-team/'



driver.get(url)
# time.sleep(6)

result = get_staff_contact_danburyVolvo(driver, url)
# yu13 = northfieldvolvo
# yui3 with no text for contact = whitebear
# 

# result = scraper_dealerOn(driver, 'https://www.andymohravonnissan.com')
# result = scraper_dealerDotCom(driver, URL10)
print("\nResult:")
print(result)

print("Result length: ", len(result))

# for url in DEALERFIRESITES:
#     print("Processing url: " + url)
#     result = scraper_dealerFire(driver, url)
#     print("\nResult:")
#     print(result)


driver.quit()