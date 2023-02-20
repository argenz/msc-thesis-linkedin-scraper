from linkedin_api import Linkedin
import logging as log 

# PURPOSE OF THIS FILE: Define methods to interact with the linkedin api

class API_Client(object): 
    def __init__(self, email, pwd) -> None:
        self.api = Linkedin(email, pwd)
        self.unidentified_companies = []
        self.unidentified_people = []
    
    #def search_people(self, firstname, lastname, companies_urn_ids=[]): 
    #    if len(companies_urn_ids)==0: 
    #        return self.api.search_people(keyword_first_name=firstname, keyword_last_name=lastname) #PLAIN SEARCH
    #    else: 
    #        return self.api.search_people(keyword_first_name=firstname, keyword_last_name=lastname, past_companies=companies_urn_ids)

    # def search_people_current(self, fullname, companies_urn_ids): 
    #    return self.api.search_people(keywords=fullname, current_company=companies_urn_ids)
    
    def search_people(self, keywords): 
        return self.api.search_people(keywords=keywords)
    
    def get_profile(self, public_id: str) -> dict: 
        return self.api.get_profile(public_id)
    
    def search_and_get_profile(self, firstname: str, lastname: str, past_companies_urn_ids: list[str])->dict: 
        people = self.search_people(firstname, lastname, past_companies_urn_ids)
         
        if len(people)==0: 
            log.warning(f"There were no search results for people with this credentials: {firstname,lastname,past_companies_urn_ids}")
            self.unidentified_people.append([firstname, lastname, past_companies_urn_ids])
            return None
        else: 
            person = people[0] #Assume that the first result is the right one in every search (since we have filtered for companies).
            return self.get_profile(person["public_id"])

    #search company URN ID 
    def search_company(self, name: str): 
        return self.api.search_companies(name)
    
    def get_company_urn_id(self, name: str): 
        companies = self.search_company(name)
        if len(companies)==0:
            log.warning(f"There were no search results for companies with this name: {name}")
            self.unidentified_companies.append(name)
            return None
        else: #Assume that the first result is the right one in every search.
            company = companies[0]
            log.info(f"URN ID for comapny: {name}, is {company['urn_id']}")
            return company["urn_id"]
    
        


    

        
    

