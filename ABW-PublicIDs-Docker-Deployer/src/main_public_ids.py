from api_client import API_Client
from daos.bidders_dao import biddersDAO
from daos.companies_dao import companiesDAO
import csv
import logging as log
import numpy as np
import pandas as pd
from datetime import datetime
from indexes import start, end 
from config import email, pwd

# Once I have the list of companies and their URN IDs (companies.csv)
# PURPOSE OF THIS FILE: Obtain all public_id of people

# LOGGING Configuration ---
log.basicConfig(filename=f'logs/log_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}.log', level=log.INFO, format='%(asctime)s|%(module)s:%(lineno)s|%(levelname)s|%(message)s') 

# search for a person 
companies_dao = companiesDAO("files/companies.csv", separator=";")
bidders_dao = biddersDAO("files/bidders_2000_2020_random.csv", separator=";")
api = API_Client(email, pwd)


# Orginal file: 
bidders = bidders_dao.get_all_bankers() 

#Override end
#end = 1

bidders = bidders[start:end] 

i = start
with open(f'files/advisors_public_ids.csv', 'w') as f:
        writer=csv.writer(f, delimiter=';',lineterminator='\n',)
        writer.writerow(["index", "fullname", "public_id", "current_company"]) 

        for person in bidders: 
            log.info(f"iteration {i}: Currently searching =  Person: {person}")
            past_companies = bidders_dao.get_sequence_companies_banker(person)         
            log.info(f"Sequence companies: {past_companies}")

            public_id = np.nan
            keywords = person
        
            if len(past_companies)>0:
                current_company = past_companies[-1]
                keywords = keywords + " " + current_company
            
            log.info(f"API Request with,  Keywords: {keywords}")

            response = api.search_people(keywords=keywords)
            
            if len(response)==0: 
                log.warning(f"There were no search results for people with this credentials: {person, current_company}")

            if len(response)>0: 
                public_id = response[0]["public_id"]
                log.warning(f"FOUND - Public ID for {person} which is {public_id}")
            
            row = [i, person, public_id, current_company]
            log.info(f"ROW: {row}")
            writer.writerow(row)
            i += 1
 