from tkinter.tix import Tree
import docker 
import logging as log 
from ab_utils import write_config_py, write_indexes_py
import os

log.basicConfig(level=log.INFO, format='%(asctime)s|%(module)s:%(lineno)s|%(levelname)s|%(message)s') 

#THIS FILE IS AN AUTOMATIC DOCKER CONTAINER DEPLOYER. Actions: 
# Created and runs containers that run the public_ids search scraper on the banker with the specified index ids. 
# Waits unitl all containers are done, and saves local container files onto host at specified location.

# GLOBAL VARS: 

# the advisors indexes to search - from 0 to 43000 circa.
index_pairs = [[23766, 23767], [31483, 31485], [35629, 35685]] 

# the emails (passwords were all created equal, so only email necessary. At each run of this file, change the email. 
email = "giannirotelle@outlook.com"

app_path = os.getcwd() 
log.info(f"The APP's PATH IS: {app_path}")

client = docker.from_env()
log.info("Created docker Client.")

write_config_py(f"{app_path}/src/config.py", email)

containers = []
for pair in index_pairs: 
    start = pair[0]
    end = pair[1]

    #LOCAL CONTAINER:
    write_indexes_py(f"{app_path}/src/indexes.py", start, end)

    image_tag = f"scrp_{start}_{end}"

    client.images.build(path="/Users/fcra/Desktop/LNKDN_Scraper/ABW", tag=image_tag, rm=True) #Change to current & relevant
    log.info(f"Created Image {image_tag}")

    container = client.containers.run(image_tag, detach=True)
    log.info(f"Running contrainer from image {image_tag} with container id {container.id}")
    containers.append(container)

## FINSIH CREATING AND RUNNING ALL CONTAINERS 
# Check if any of them are done. 

for containter in containers:
    container.wait()

log.info(f"All containers sucessfully exited.")

# export local container files onto host
for index in range(len(containers)): 
    copy_cmd = f"docker cp {containers[index].id}:/usr/app/src/files/advisors_public_ids.csv /Users/fcra/Desktop/exports/advisors_public_ids_{index_pairs[index][0]}_{index_pairs[index][1]}.csv "
    os.system(copy_cmd)
    log.info(f"Exported files from {containers[index].id}.")

log.info(f"All containers succerfully executed and files exported.")

