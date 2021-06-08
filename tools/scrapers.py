
from selenium.webdriver.common.by import By
import re
from copy import deepcopy


# The phone pattern that regular expression will use to match on the page text
PHONEPATTERN = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}?')

# Pattern to check for emails
EMAILPATTERN = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


'''

THIS FILE JUST CONTAINTS NICHE SCRAPERS MADE FOR INDIVIDUAL WEBSITES.

THE TEMPLATES ARE VERY SIMILAR AND CAN BE QUICKLY CHANGED (<3 MINS) FOR EACH SITE YOU'D LIKE TO SCRAPE


'''


def get_staff_contact_carsGuam(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'staff-item':
                    staffList.append(element)
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                employee_card_children = employeeCard.find_elements(By.XPATH, './/*')
                for element in employee_card_children:
                    l = employeeCard.text.split('\n')
                    try:
                        if 'email-button' in element.get_attribute('class'):
                            name = element.get_attribute("data-staff-name")
                            email = element.get_attribute('href')
                            title = element.get_attribute('data-staff-title')
                            # print("Name: ", name, ' Title: ', title, ' Email: ', email)
                        
                        elif element.get_attribute('class') == 'staffphone':
                            
                            try:
                                phone = element.text
                                phone = re.search(PHONEPATTERN, phone).group()
                            except:
                                phone = None
                            print("2 Name: ", name, ' Title: ', title, ' Email: ', email) 
                        
                    except Exception as e:
                        print(e)
                        continue
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '':
                    continue
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    tempEmployeeContact['phone'] = None
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



def get_staff_contact_volvoWhitePlains(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == ' ddc-content content-default':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList[1:]:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')

                name = l[0]
                title = l[1]
                email = l[2].lower()
                phone = l[3]
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '':
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                tempEmployeeContact['email'] = email.replace("mailto:", "")
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


def get_staff_contact_koonsVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                txt = employeeCard.text
                l = txt.split('\n')

                name = l[0]
                title = l[1]
                try:
                    email = re.search(EMAILPATTERN, txt).group()
                except:
                    email = None

                try:
                    phone = re.search(PHONEPATTERN, txt).group()
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
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                tempEmployeeContact['email'] = email.replace("mailto:", "")
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

def get_staff_contact_cherryHillVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if 'volvo-cherry-staff-member' in element.get_attribute('class'):
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                txt = employeeCard.text
                l = txt.split('\n')
                print(l)

                name = l[0]
                title = l[1]
                try:
                    email = re.search(EMAILPATTERN, txt).group()
                except:
                    email = None

                try:
                    phone = re.search(PHONEPATTERN, txt).group()
                except:
                    phone = None

                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '' or (phone is None and email is None):
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                # print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None

def get_staff_contact_berwynVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                


                email = None



                try:
                    name = employeeCard.text
                except:
                    name = None
                
                try:
                    phone = employeeCard.find_element(By.CLASS_NAME, 'phone').get_attribute('innerHTML')
                except:
                    phone = None
                
                try:
                    title = employeeCard.find_element(By.CLASS_NAME, 'title').get_attribute('innerHTML')
                except:
                    title = None
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '' or (phone is None and email is None):
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                # print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None

def get_staff_contact_midlothianVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                


                try:
                    email = employeeCard.find_element(By.CLASS_NAME, 'email').get_attribute('innerHTML')
                except:
                    email = None



                try:
                    name = employeeCard.text
                except:
                    name = None
                
                try:
                    phone = employeeCard.find_element(By.CLASS_NAME, 'phone').get_attribute('innerHTML')
                except:
                    phone = None
                
                try:
                    title = employeeCard.find_element(By.CLASS_NAME, 'title').get_attribute('innerHTML')
                except:
                    title = None
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '' or (phone is None and email is None):
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "").replace('\n', '')
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                # print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None

def get_staff_contact_findlayVolvoCars(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                


                try:
                    email = employeeCard.find_element(By.CLASS_NAME, 'email').get_attribute('innerHTML')
                except:
                    email = None



                try:
                    name = employeeCard.text
                except:
                    name = None
                
                try:
                    phone = employeeCard.find_element(By.CLASS_NAME, 'phone').get_attribute('innerHTML')
                except:
                    phone = None
                
                try:
                    title = employeeCard.find_element(By.CLASS_NAME, 'title').get_attribute('innerHTML')
                except:
                    title = None
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '' or (phone is None and email is None):
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "").replace('\n', '')
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                # print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None


def get_staff_contact_northfieldVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                print(l)


                try:
                    emailText = employeeCard.find_element(By.CLASS_NAME, 'email').get_attribute('innerHTML').lower()
                    # email = emailText
                    email = re.search(EMAILPATTERN, emailText).group()
                except:
                    email = None



                try:
                    name = l[1]
                except:
                    name = None
                
                try:
                    phone = employeeCard.find_element(By.CLASS_NAME, 'phone').get_attribute('innerHTML')
                except:
                    phone = None
                
                try:
                    title = l[0]
                except:
                    title = None
                
                # name = employeeCard.find_element(By.CLASS_NAME, 'staff-title h3 margin-top-x').get_attribute("name")
                # # print("Name:", name)
                # # title = employeeCard.find_element(By.CLASS_NAME, 'title').text
                # title = employeeCard.find_element(By.CLASS_NAME, 'staff-desc margin-bottom_5x').get_attribute('innerHTML')
                # phone = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm phone1 phone-alert').get_attribute('href')
                # email = employeeCard.find_element(By.CLASS_NAME, 'btn btn-main btn-sm email').get_attribute('href')

                # Don't append useless data without a name
                if name is None or name == '':
                    continue
                
                print("Name: ", name, ' Title: ', title, ' Email: ', email, ' Phone: ', phone)
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                if email is not None:
                    tempEmployeeContact['email'] = email.replace("mailto:", "").replace('\n', '')
                
                if phone is not None:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                
                # print('\n Name: ', name, ' title: ', title, ' email: ', email, ' phone: ',phone, '\n')
                resultList.append(deepcopy(tempEmployeeContact))
            except Exception as e:
                # print(e)
                continue
        return resultList
    except Exception as e:
        print("Staff list not found")
        print(e)
        return None

def get_staff_contact_danburyVolvo(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if 'staff-item' in element.get_attribute('class'):
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                print(l)
                name = l[0]
                title = l[1]
                try:
                    email = None
                except:
                    email = None
                try:
                    phone = l[2]
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
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    phone = None
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
    


def get_staff_contact_noContact(driver, url):
    resultList = []
    # driver.find_element(By.XPATH, '/html/body/main/section/div[3]/section[1]/div[2]/ul/li[4]/a').click()
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'advisor-card-content ng-scope':
                    
                    staffList.append(element)
                    # print(element.text)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        print("Number of employees: ", len(staffList))
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                # print(l)
                try:
                    # name = l[0]
                    name = employeeCard.find_element(By.XPATH, './/div[3]/div/div[1]').text
                    # print(name)

                    # name = employeeCard.find_element(By.CLASS_NAME, 'advisor-name ng-binding').text
                    # name = employeeCard.find_element(By.CSS_SELECTOR,'div.staff-title.h3.margin-top-x').get_attribute('innerHTML')
                except Exception as e:
                    # print(e)
                    # name = employeeCard.find_element(By.XPATH, '//h3').get_attribute('innerHTML')
                    name = None
                try:
                    # title = l[1]
                    title = employeeCard.find_element(By.XPATH, './/div[3]/div/div[2]').get_attribute('innerHTML')

                    # title = employeeCard.find_element(By.CLASS_NAME, 'advisor-title ng-binding').text
                    # title = employeeCard.find_element(By.XPATH, '//div[2]/em').get_attribute('innerHTML')
                except:
                    # title = employeeCard.find_element(By.XPATH, '//p').get_attribute('innerHTML')
                    title = None
                try:
                    emailtxt = employeeCard.find_element(By.CLASS_NAME, 'link').get_attribute('innerHTML').lower()
                    email = re.search(EMAILPATTERN, emailtxt).group()
                except Exception as e:
                    # print(e)
                    email = None
                try:
                    phonetxt = employeeCard.find_element(By.XPATH, './/div[2]/div[2]/div[2]/div[2]/a[1]').get_attribute('href')
                    # phonetxt = employeeCard.find_element(By.CLASS_NAME, 'gfx-phone-link ng-isolate-scope').get_attribute('href')
                    phone = re.search(PHONEPATTERN, phonetxt).group()
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
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    phone = None
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


def get_staff_contact_communityCars(driver, url):
    resultList = []

    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'staff-directory-link':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                # print(l)
                try:
                    name = l[0]
                    # name = employeeCard.find_element(By.CSS_SELECTOR,'div.staff-title.h3.margin-top-x').get_attribute('innerHTML')
                except:
                    # print(e)
                    name = employeeCard.find_element(By.XPATH, '//h3').get_attribute('innerHTML')
                try:
                    title = l[1]
                    # title = employeeCard.find_element(By.XPATH, '//div[2]/em').get_attribute('innerHTML')
                except:
                    title = employeeCard.find_element(By.XPATH, '//p').get_attribute('innerHTML')
                try:
                    emailtxt = employeeCard.find_element(By.CLASS_NAME, 'link').get_attribute('innerHTML').lower()
                    email = re.search(EMAILPATTERN, emailtxt).group()
                except Exception as e:
                    # print(e)
                    email = None
                try:
                    phonetxt = employeeCard.find_element(By.CLASS_NAME, 'link').get_attribute('innerHTML')
                    phone = re.search(PHONEPATTERN, phonetxt).group()
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
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    phone = None
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


def get_staff_contact_jacobsMitsu(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 've-col-xs-12 employee-details ve-pad-top-md ve-pad-bottom-none ve-pad-right-md':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                print(l)

                name = l[0]
                title = l[1]
                try:
                    # email = l[2].lower()
                    email = None
                except:
                    email = None
                try:
                    phone = l[2]
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
                    continue
                
                
                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    phone = None
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

def get_staff_contact_whiteBearMitsu(driver, url):
    resultList = []
    try:
        # Get all elements
        all_elements = driver.find_elements(By.XPATH, './/*')
        staffList = []
        for element in all_elements:
            try:
                if element.get_attribute('class') == 'yui3-u-1-6 staff':
                    staffList.append(element)
                    # print('\n',element.text,'\n')
            except:
                continue
        # staffList = driver.find_elements_by_class_name('staff-card col-md-4 col-sm-6')
        # print("StaffList: ", staffList)
        for employeeCard in staffList:
            try:
                tempEmployeeContact = {'name': None, 'position': None, 'email': None, 'phone': None}
                # print("Found employee tile: " , employeeCard.get_attribute('innerHTML'))
                l = employeeCard.text.split('\n')
                # print(l)
                # name = l[0]
                # title = l[1]
                name = employeeCard.find_element(By.XPATH, './/dl/dt/a').get_attribute('name')
                title = employeeCard.find_element(By.XPATH, './/dl/dd[1]').get_attribute('innerHTML')
                try:
                    email = employeeCard.find_element(By.XPATH, './/dl/dd[3]').get_attribute('innerHTML')
                except:
                    email = None
                try:
                    phone = employeeCard.find_element(By.XPATH, './/dl/dd[4]').get_attribute('innerHTML')
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
                    continue

                tempEmployeeContact['name'] = name
                tempEmployeeContact['position'] = title
                try:
                    tempEmployeeContact['email'] = email.replace("mailto:", "")
                except:
                    tempEmployeeContact['email'] = None
                try:
                    tempEmployeeContact['phone'] = phone.replace("tel:", '')
                except:
                    phone = None
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