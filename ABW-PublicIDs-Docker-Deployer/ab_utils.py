import os
import logging as log 

####### Function to write indexes.py and config.py 

def write_indexes_py(file_path_name, start, end):
    with open(file_path_name, 'w') as f:

        f.write(f'''\
start = {start}
end = {end}       
''')
    log.info(f'Written new indexes.py file with start: {start}, end {end}.')

#
def write_config_py(file_path_name, email, pwd):
    with open(file_path_name, 'w') as f:

        f.write(f'''\
email = "{email}"
pwd = "{pwd}"     
''')

    log.info(f'Written new config.py with email {email}')

##### Fucntion to copy file form container to host
