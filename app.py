import sys
from flask import Flask, render_template, request
from src.utils.common_utils import save_as_jpg, push_to_mongodb
from src.get_images import ImagesFromGoogle

from src.logger import logging
from src.exception import CustomException

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            search_item = request.form['content'].replace(" ", "")

            image_scrapper = ImagesFromGoogle(search_item)
            urls = image_scrapper.get_image_urls()

            save_as_jpg(urls)
            push_to_mongodb(urls=urls)

            return "images loaded"
        
        except Exception as e:
            logging.error("Error occured on /review route!")
            raise CustomException(e, sys)
    else:
        return render_template('index.html')
    
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000)

