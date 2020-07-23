FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt 
EXPOSE 8080
CMD python3 main.py 