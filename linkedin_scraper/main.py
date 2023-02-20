import csv
import sys
import time
from api_client import API_Client
from daos.bidders_dao import biddersDAO
from daos.companies_dao import companiesDAO
from scraper import Scraper
import logging as log
from datetime import datetime
import pandas as pd 
from mydriver import mydriver
from checkpoint import checkpoint 
from utils import write_in_restricted

log.basicConfig(filename=f'logs/log_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}.log', level=log.INFO, format='%(asctime)s|%(module)s:%(lineno)s|%(levelname)s|%(message)s') 

# Get list of fake accounts that the script can iterate through if they get restricted by LinkedIn
accounts = pd.read_csv("./files/accounts.csv", sep=";")

# Data Access Object for bankers
bidders = biddersDAO("files/bidders_2000_2020_random.csv")

# For each account
for row in accounts.iterrows(): 
    # take account info from tuple
    account = row[1]
    # get email of account
    email = account["Email"]

    # Check if account is in restricted list 
    restricted = pd.read_csv("./files/accounts_restricted.csv", sep=";")
    restricted_list = restricted["Email"].tolist()

    log.info(f"Checking if {email} is in restricted_accounts.csv.")

    # If email is in restricted accounts, proceed to next account 
    if email in restricted_list: continue 
    
    # If proceeds with current, means account is not in list. So take the password. 
    pwd_linkedin = account["Password"]
    pwd_email = account["Linkedin password"] #yes, they are right. The excel provided is wrong.

    # Open Selenium Webdriver and Verify Linkedin account
    driver = mydriver()
    isrestricted = driver.login_and_verify_account(email, pwd_linkedin, pwd_email) 

    # If account is restricted, write in restricted list and proceed with next account
    if isrestricted: 
        write_in_restricted(restricted, row)
        driver.quit()
        continue

    # If proceeds, then account is not restricted and has been verified.
    # Try opening connection to Linkedin API. 
    iter = 0
    while iter<30:  #Attempt thirty times while the browser is opened. 
        try: 
            log.info(f"Trying login number {iter}.")
            api = API_Client(email, pwd_linkedin)
            iter = 30

        except Exception as e: 
            log.info(f"Not successful: {e}")
            iter = iter+1
            #time.sleep(1)
    
    # Finally execute the scraping of the profiles with the public IDs
    exit_code = 1 
    try: 
        # Open connection to scraper 
        scraper = Scraper(bidders, api)

        # Downloading profiles
        exit_code, checkpoint = scraper.write_json_profiles_in_folder("files/all_advisors_False.csv", "profiles", checkpoint, 11679) 

        log.info(f"Writing account {email} to restricted csv.")
        write_in_restricted(restricted)

        if exit_code == 0: sys.exit("Process Completed.")

    except Exception as e: 
        log.info(f"Not successful at initialising Linkedin API. Because: {e}. Continuing onto next profile.")

    driver.quit()

    
    

