from datetime import datetime
import json
import sys
import csv
import logging as log
import numpy as np
import pandas as pd

# In this class are defined the logical methods to search for companies, public_ids, and profiles. 
# They use the basic methods of the API_Client (search_people, get_profile) but are nested in the 
# layers of logic required for finding the right person and the right profile. 

class Scraper(object): 
    def __init__(self, biddersDAO, API_Client):
        self.biddersDAO = biddersDAO 
        self.API_Client = API_Client

    # Write public ids
    def write_public_ids_keywords(self, write_to_path, start_index, end_index):
        if self.companiesDAO==None: 
            sys.exit("You need to pass the companiesDAO (Data Access Object) from the companies.csv file. If you don't have companies.csv, you can create it from the method 'write_comapnies_csv' from this class.")

        bidders = self.biddersDAO.get_all_bankers()[start_index:end_index]

        i = start_index
        with open(write_to_path, 'w') as f:
            writer=csv.writer(f, delimiter=';',lineterminator='\n',)
            writer.writerow(["index", "name", "surname", "public_id", "plain_search"]) 

            for person in bidders: 
                log.info(f"iteration i = {i}")
                past_companies = self.biddersDAO.get_sequence_companies_banker(person)

                public_id = np.nan

                # TAKE ONLY LAST COMPANY IN LIST 
                current_company = past_companies[-1]
                keywords = person + " " + current_company
                
                #iterative search
                log.info(f"Currently searching =  Person: {person}, Companies: {current_company}")

                response = self.API_Client.search_people(keywords=keywords)
                
                if len(response)==0: 
                    log.warning(f"There were no search results for people with this credentials: {person, current_company}")

                if len(response)>0: 
                    # take first result
                    public_id = response[0]["public_id"]
                    log.warning(f"FOUND - Public ID for {person} which is {public_id}")
                
                row = [i, person, public_id, current_company]
                log.info(f"ROW: {row}")
                writer.writerow(row)
                i += 1


    # retrieve JSON profiles and write them in folder 
    def write_json_profiles_in_folder(self, public_ids_csv_path, write_to_folder, start, end):
        public_ids_df = pd.read_csv(public_ids_csv_path)
        public_ids_df = public_ids_df.loc[start:end]
    
        # comment to self: Not very good architecture because depends on fixed structure of "all_advisors_False" file, but ok.
        for advisor in public_ids_df.iterrows(): 
            public_id = advisor[1][4]
            index = advisor[1][1]
            new_index = advisor[1][0]

            log.info(f"Currently retrieving profile {index} with public id: {public_id}")
            try: 
                profile = self.API_Client.get_profile(public_id)

            except Exception as e: 
                with open("checkpoint.py", 'w') as f:
                    f.write(f'''\
checkpoint = {new_index}    
''')            
                return 1, new_index # Exit code

            try:
                log.info(f"Retrieved profile with index {new_index}, public_id: {public_id}, has headline: {profile['headline']}")
            except:
                log.info(f"Retrieved profile with index {new_index}, public_id: {public_id}, but has no headline.")

            # Writing to folder 
            with open(f'{write_to_folder}/{new_index}_{index}_{public_id}.json', 'w') as fp:
                json.dump(profile, fp)

        log.info("Execution completed.")
        return 0, new_index # Exit code


    


            



