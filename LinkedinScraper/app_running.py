from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import render_template
import logging

from scrapingLinkedin import *
from wordCloud import *

app = Flask(__name__)

# Configura il logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting app..")

@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')

@app.route('/test', methods=['GET'])
def test():
    return "Everything is working fine"



@app.route('/WordCloud', methods=['POST'])
def scraping():
    if request.method =='POST':
        content = request.json
        jobTitle,location = content['jobTitle'].lower(),content['location'].lower()
        print(f'Running scraping for the job: {jobTitle} in {location}')
        scrapingLinkedin(jobTitle, location)
        print('Scraping fatto ora creo la wordCloud')
        wordCloud(jobTitle, location)
        return {'jobTitle':jobTitle, 'location':location }
    else:
        return 'This method is not allowed', 400

@app.route('/WordCloudlandingpage', methods=['GET','POST'])
def WordCloudlandingpage():
    jobTitle = request.args.get('jobTitle', 'N/A').lower().replace(" ",'_')
    location = request.args.get('location', 'N/A').lower()
    path_to_image = f'../static/Images/{location}_{jobTitle}.png'
    print(path_to_image) 
    return render_template('wordCloudLandingPage.html', jobTitle=jobTitle.capitalize(), location=location.capitalize(), path_to_image=path_to_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=False)