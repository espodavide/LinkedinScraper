
FROM selenium/standalone-chrome:latest

RUN sudo apt-get update && sudo apt-get install -y python3-pip

WORKDIR /Linkedin

COPY . ./

RUN sudo pip install --trusted-host pypi.python.org -r requirements.txt
RUN sudo /usr/bin/python3 -m nltk.downloader stopwords
RUN sudo /usr/bin/python3 -m nltk.downloader punkt

EXPOSE 8080
CMD ["sudo","/usr/bin/python3", "app_running.py"]
