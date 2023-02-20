import csv

# Writes file of restricted accounts each time a new account gets restricted 
def write_in_restricted(restricted, row): 
    #write profile in restricted accounts
    with open("./files/accounts_restricted.csv", 'w') as f:
        writer=csv.writer(f, delimiter=';',lineterminator='\n',)
        writer.writerow(["First name","Last name","Email","Password","Linkedin password","Phone number","Recovery email","Url","","","","","","","","","","","","","","","","",""])
        for row_restr in restricted.iterrows(): 
            writer.writerow(row_restr[1].tolist()) 
        writer.writerow(row[1].tolist()) 