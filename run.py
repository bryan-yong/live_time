# LiveTime Work-Stoppage Notifier

import json
import time
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Opens JSON file for credentials and inputs into appropriate fields
def login():
    credentials = 'PATH TO YOUR credentials.json FILE'
    driver.get('REMOVED URL')
    
    # Waits to see login fields appear on page before finally logging in
    # if login in field is never found webdriver will redirect to login page
    # finally will login to account with stored credentials
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/form/input[1]'))
        )
    except:
        driver.get('REMOVED URL')
    
    finally:
        with open(credentials, 'r') as data:
            info = json.load(data)
            uidInput = driver.find_element_by_xpath('/html/body/div/form/input[1]')
            passInput = driver.find_element_by_xpath('/html/body/div/form/input[2]')
            uidInput.send_keys(info['user'])
            uidInput.send_keys(Keys.TAB)
            passInput.send_keys(info['pass'])
            passInput.send_keys(Keys.ENTER)

# Opens incidents page via clicking on 'Operations' using ActionChain
def incidents():
    # Waits to see if the drop menu icon is present on page
    # if not it will call the login() function
    # Once login function has finished it will finally bring page to incidents page
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-nav-icon"]'))
        )
    except:
        login()
    finally:
        dropMenu = driver.find_element_by_xpath('//*[@id="main-nav-icon"]')
        operations = driver.find_element_by_xpath('//*[@id="menu-main-ul"]/li[2]/ul/li[1]/h3/a/span')
        dropMenu.click()
        dropMenu.click()
        operations.click()

# Takes in alert variable which is a tuple by default and converts it into a string 
# and formats it into preferred message form then sends an alert to given address
def send_alert(alert):
    # Defines path to where credentials are stored in a json file
    # Then opens the json file as read to grab data for credentials
    credentials = 'PATH TO YOUR credentials.json FILE'
    with open(credentials, 'r') as data:
        info = json.load(data)
        user = info['email']
        epass = info['epass']
        formatted = str(alert)[1:-1]
        # Formats email/text body
        msg = EmailMessage()
        msg.set_content(formatted.replace(',', '\n'))
        msg['Subject'] = 'WORK STOPPAGE DETECTED'
        msg['From'] = user
        msg['To'] = 'email address(es) or phone number(s)'
        # Creates a local SMTP_SSL server to send message from service account to stored address
        # Then closes server once message is sent
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo() 
            server_ssl.login(user, epass)
            server_ssl.send_message(msg)
            server_ssl.close()
            print('Alert has been sent')
        except:
            print('Something went wrong...')
            
# Scans tickets for key phrases
def scan():
    # HTML class names inside scrolling list alternate between 'normalRow' and 'alternateRow'
    # This stores the text from corresponding elements and looks for strings that match key phrases
    tickets = []
    phrases = ['workstoppage', 'work stoppage', 'work-stoppage']
    
    # Waits to see if ticket queue element is present on page before finally scanning queue for tickets containing key phrases
    # If element is never found calls incidents function
    # after exception is triggered to call incidents function, it will scan queue for key phrases
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="scrollingList"]/tbody[1]'))
    )
    except:
        incidents()
    
    finally:    
        
        normalRows = driver.find_elements_by_class_name('normalRow')
        for row in normalRows:
            text = row.text.split('\n')
            tickets.append(text)
        
        altRows = driver.find_elements_by_class_name('alternateRow')
        for row in altRows:
            text = row.text.split('\n')
            tickets.append(text)
        
        # If key phrase is found it will check to see if it is cached already
        # If not cached it will cache alert in new list and send alert
        for ticket in tickets:
            for item in ticket:
                for phrase in phrases:
                    if phrase in item.lower():
                        alert = ticket[0], ticket[1], ticket[6], ticket[7], ticket[10], ticket[11]
                        if alert in alerts:
                            print('Already present')
                            continue
                        else:
                            send_alert(alert)
                            alerts.append(alert)
                            continue
                    else: continue

# Compares cached tickets to current queue
def checkCache():
    # HTML class names inside scrolling list alternate between 'normalRow' and 'alternateRow'
    # This stores the text from corresponding elements and looks for strings that match key phrases
    tickets = []
    cache = []
    phrases = ['workstoppage', 'work stoppage', 'work-stoppage']
    
    # Waits to see if the ticket queue is present on page before finally checking if cached alerts are removed from queue
    # If cached ticket is not found on queue, removes ticket from cached list
    # if ticket queue element not found on current page, calls the incidents function to return to queue then scans
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="scrollingList"]/tbody[1]'))
    )
    except:
        incidents()
    
    finally:
        
        normalRows = driver.find_elements_by_class_name('normalRow')
        for row in normalRows:
            text = row.text.split('\n')
            tickets.append(text)
        
        altRows = driver.find_elements_by_class_name('alternateRow')
        for row in altRows:
            text = row.text.split('\n')
            tickets.append(text)
        
        # If key phrase is found it will check to see if it is cached already
        # If not cached it will cache alert in new list
        for ticket in tickets:
            for item in ticket:
                for phrase in phrases:
                    if phrase in item.lower():
                        alert = ticket[0], ticket[1], ticket[6], ticket[7], ticket[10], ticket[11]
                        cache.append(alert)
        # Checks to see if tickets in cached list are on queue
        # If not in queue then deletes it from cached list
        for ticket in alerts:
            if ticket in cache:
                print('Found')
                continue
            else:
                alerts.remove(ticket)
                print('Ticket has been removed from queue.')
                continue

# Opens webbrowser as driver
driver = webdriver.Chrome()

# List for any tickets that trigger condition
alerts = []
