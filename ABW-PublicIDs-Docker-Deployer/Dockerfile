FROM ubuntu:latest

RUN apt update 
RUN apt install python3 -y
RUN apt -y install python3-pip
RUN apt install vim -y
RUN apt-get install sudo -y

WORKDIR /usr/app/src

COPY src ./ 

RUN pip3 install -r req.txt

CMD ["python3", "main_public_ids.py"]

