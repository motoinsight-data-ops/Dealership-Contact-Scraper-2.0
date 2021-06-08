from selenium.webdriver.common.by import By
import re
from copy import deepcopy
from collections import Counter


# The phone pattern that regular expression will use to match on the page text
PHONEPATTERN = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}?')

# Pattern to check for emails
EMAILPATTERN = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


def scanForSiteMap(driver, url):
    """
    -------------------------------------------------------
    Scans home page of dealer site for a site map, returns True is found and False if not found.
    -------------------------------------------------------
    Args: 
    Driver: Selenium Web Driver - The web driver passed in should already be at the dealership home page.
    Url: Str - The url of the dealer sites home page
        
    Returns: 
        True if a site map is found
        False if not
            
    ------------------------------------------------------
    """
    # Get all elements of page to iterate through and find the sitemap
    elems = driver.find_elements(By.XPATH, './/*')
    completed = 0
    for elem in elems:
        try:
            # Try getting the elements href attribute
            href = elem.get_attribute('href').lower()
            completed = 0
            
            # See if href contains substring with sitemap in it.
            if ('site' in href and 'map' in href) and 'xml' not in href:
                completed = 1
                # Navigate driver to dealerships sitemap
                print("Sitemap found for "+ url)
                driver.get(href)
                return True
            
        # If it can't get href from this element, go to the next
        except:
            continue
    # If scan through all elements and no sitemap link found
    if completed == 0:
        print("No sitemap found for " + url)
        return False


def scanForStaffPage(driver, url):
    """
    -------------------------------------------------------
    Scans site map for 
    -------------------------------------------------------
    Args: 
    Driver: Selenium Web Driver - The web driver passed in should already be at the dealership site map page.
    Url: Str - The url of the dealer sites home page
        
    Returns: 
        True if a staff page is found
        False if not
            
    ------------------------------------------------------
    """
    # Get all elements of page to iterate through and find the staff page
    elems = driver.find_elements(By.XPATH, './/*')
    completed = 0
    for elem in elems:
        try:
            # Try getting the elements href attribute
            href = elem.get_attribute('href').lower()
            completed = 0
            
            # See if href contains substring with sitemap in it.
            if 'staff' in href or 'team' in href and 'join' not in href and 'velocity' not in href:
                print("Staff page found for " + url)
                completed = 1
                # Navigate driver to dealerships sitemap
                driver.get(href)
                
                return True
            
        # If it can't get href from this element, go to the next
        except:
            continue
    # If scan through all elements and no sitemap link found
    if completed == 0:
        print("No staff page found for " + url)
        return False

def findSalesDepPhoneNumber(driver, url):

    """
    -------------------------------------------------------
    Scans home page of dealer site for the sales department contact phone number.
    -------------------------------------------------------
    Args: 
    Driver: Selenium Web Driver - The web driver passed in should already be at the dealership home page.
    Url: Str - The url of the dealer sites home page
        
    Returns: 
        Number (str) if a phone number is found
        None if not
            
    ------------------------------------------------------
    """

    # First try to find first HREF to tel

    elems = driver.find_elements(By.XPATH, './/*')

    for elem in elems:
        try:
            # Try getting the elements href attribute
            href = elem.get_attribute('href').lower()
            
            # See if href contains substring with sitemap in it.
            if 'tel' in href:
                
                # Extract phone number from href
                firstMatch = re.search(PHONEPATTERN, href)
                print("Phone number found: " + firstMatch.group())
                return firstMatch.group()
            
        # If it can't get href from this element, go to the next
        except:
            continue

    # If scan through all elements and no sitemap link found, try to find phone number in raw text



    # Get entire web page
    page = driver.find_element(By.TAG_NAME, 'body')

    # Get just the raw text of the page
    pageText = page.text
    # print(pageText)

    

    # Get first match
    firstMatch = re.search(PHONEPATTERN, pageText)

    if firstMatch != None:
        firstMatch = firstMatch.group()
    else:
        return None

    # If return string is empty, set return value to None
    if firstMatch == '':
        firstMatch = None
        print("Sales number not found")
    else:
        print("Sales number: " + firstMatch)

    return firstMatch


def scraper_Common(driver, url):
    result = {'Staff Page': None, 'Sales': None, 'Staff Contact':None}
    try:
        driver.get(url)
    except: 
        result = {'Staff Page': 'NOT REACHABLE', 'Sales': 'NOT REACHABLE', 'Staff Contact': 'NOT REACHABLE'}
        print(url + " not reachable.")
        return result

    # Find sales department phone number
    salesDepNumber = findSalesDepPhoneNumber(driver, url)
    result['Sales'] = salesDepNumber
    
    # Variable to hold whether the site has a sitemap or not
    siteMapAvailable = scanForSiteMap(driver, url)

    # Variable to hold whether the site has a staff page or not
    staffPageAvailable = False

    if siteMapAvailable:
        staffPageAvailable = scanForStaffPage(driver, url)
        result['Staff Page'] = staffPageAvailable
    else:
        return result

    staffEmailsAvailable = False
    if staffPageAvailable:
        staffEmailsAvailable = checkForEmail(driver, url)
    
    result['Staff Contact'] = staffEmailsAvailable
    
    return result


def get_staff_contact_common(driver, url):
    resultList = []

    class_name_list = []

    STAFF_TILE_CONTENT_WHITELIST = ['yui','staff', 'member', 'employee', 'col-', 'team']

    STAFF_TILE_CONTENT_BLACKLIST = ['wrapper', 'name', 'img', 'image']

    TITLE_WHITELIST = ['service', 'finance', 'general', 'new', 'used', 'internet', 'parts', 'sales', 'wholesale', 'client', 'owner', 'executive', 'bdc', 'rental', 'tech', 'consultant', 'certified', 'assistant']

    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                # Add the class name of all the elements on the page to find out the most common (staff tile) element class name
                if any(keyWord in element.get_attribute('class').lower() for keyWord in STAFF_TILE_CONTENT_WHITELIST) and not any(keyWord in element.get_attribute('class').lower() for keyWord in STAFF_TILE_CONTENT_BLACKLIST):
                    # print(element.get_attribute('class').lower())
                    class_name_list.append(element.get_attribute('class').lower())
            except:
                continue
        
        # Create a counter to count occurences of class names
        counter = Counter(class_name_list)
        # Get most common class name
        staff_tile_class_name = counter.most_common(1)[0][0]
        print('Most Common Element: ', staff_tile_class_name)
        # Next, append all the elements with the staff tile name
        for element in all_elements:
            try:
                if element.get_attribute('class').lower() == staff_tile_class_name:
                    staffList.append(element)
            except:
                continue

        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                outerHTML = employeeCard.get_attribute('outerHTML').lower()
                txt = employeeCard.text.lower()
                l = txt.split('\n')
                # print(l)
                print(txt)
                quit

                name = l[0]
                title = l[1]
                try:
                    email = re.search(EMAILPATTERN, outerHTML).group()
                except:
                    email = None

                try:
                    phone = re.search(PHONEPATTERN, outerHTML).group()
                except:
                    phone = None

                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '':
                    print("NAME IS NONE??")
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)

                # Check if name contains one of the title keywords. If so, reverse name and title as they were in opposite orders as specified.
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title

                if any(keyWord in name.lower() for keyWord in TITLE_WHITELIST):
                    tempEmployeeContact['name'] = title
                    tempEmployeeContact['position'] = name


                
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None