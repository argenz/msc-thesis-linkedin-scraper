import pandas as pd
import numpy as np 

class companiesDAO(object): 
    def __init__(self, path, separator) -> None:
        self.data = pd.read_csv(path, sep=separator)
    
    # Single company name 
    def get_company_urn_id(self, name): 
        #name contains string name 
        name = str.lower(name)
        result = self.data[self.data.company == name] #self.data.query(f'company == "{name}" ')
        return result.iloc[0]['urn_id']
    
    # List of companies names 
    def get_companies_urn_ids(self, listnames):
        urn_ids = []
        for company in listnames: 
            urn_ids.append(self.get_company_urn_id(company))
        return urn_ids