import pandas as pd 
from itertools import groupby 


class biddersDAO(object): 
    def __init__(self, path, separator=";") -> None:
        self.data = pd.read_csv(path, sep=separator, header=0)

        # Preprocessing of "current house" (i.e. company) to enable smoother API search
        self.data['current_house'].replace({ r"[,;0-9\f\t\v\s]+$" : '' }, inplace= True, regex = True)
        substrings = ['limited', 'inc', 'ltd', 's.r.l', 'llc', 'gmbh', 'llp', 'b.v', 'plc', '~', 's.a.s', 'spa', 's.p.a', 's.a', 'sarl', 'corp', 'cpa', 'l.p', 'pte', 'sa', 'as', 'pvt', 'pty', 'nv', 'ab', 'ao', 'sro', 'ag']
        self.data['current_house'] = self.data['current_house'].str.lower()
        for substring in substrings:
            self.data['current_house'].replace(fr"\b\(?{substring}\)?\.?\s?\b", '', inplace= True, regex = True)  #removes any of the substrings above if they are standalone, and also if they are followed by . \s or within ()
        self.data['current_house'].replace(r"\b[\.,\~]\b", '', inplace= True, regex = True) #removes random . , or ~ in the middle
        self.data['current_house'].replace(r"[\s\.,\~]*$", '', inplace= True, regex = True) #removes whitespaces at end


    # returns a list of companies in which the bankers has closed a deal
    def get_sequence_companies_banker(self, name): 
        person_career =  self.data[self.data.advisor == name].sort_values("deal_year")   
        person_companies = person_career.loc[:, "current_house"].tolist()
        return [ k for k, _ in groupby(person_companies)]
    
    def get_all_companies(self): 
        companies = self.data.loc[:,["current_house"]]
        return companies.groupby("current_house").sum().index.tolist()

    def get_all_bankers(self): 
        bankers = self.data.loc[:, ["advisor"]]
        return bankers.groupby("advisor").sum().index.tolist()




    

        


