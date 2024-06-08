import os
import sys
import requests
from pymongo.mongo_client import MongoClient

from src.logger import logging
from src.exception import CustomException



def save_as_jpg(urls: list[dict]):
    try:
        logging.info("saving query images as jpg")

        query_item = None
        save_dir = "scrapped_images"
        for url in urls:
            query_item = list(url.keys())[0].split('_')[0]
            for filename, image_url in url.items():
                file_dir = os.path.join(save_dir, query_item)
                os.makedirs(file_dir, exist_ok=True)

                image_data = requests.get(image_url).content
                with open(os.path.join(save_dir, query_item, filename + ".jpg") , "wb") as f:
                        f.write(image_data)

        logging.info(f"saved images as jpg at {save_dir}/{query_item}")

    except Exception as e:
        logging.error("failed to save images as jpg")
        raise CustomException(e, sys)
    

def push_to_mongodb(urls: list):
    try:
        try:
            logging.info("Creating mongoDB client:")
            # upadte username and password here
            client = MongoClient("mongodb+srv://<username>:<password>@cluster0.90eolay.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            if client.admin.command('ping'):
                logging.info("Pinged your deployment. You successfully connected to MongoDB!")

                db = client['image_scrap']
                dataset = db['image_scrap_data']
                
                logging.info("inserting urls into: image_scrap dataset")
                dataset.insert_many(urls)
                logging.info(f"Loaded {len(urls)} items to image_scrap_data!")

        except Exception as e:
            logging.error("Couldn't establish mongoDB connection!")
            raise CustomException(e, sys)
        
        
    
    except Exception as e:
        logging.error('Failed to load data to image_scrap dataset on mongoDB!')
        raise CustomException(e, sys)
    

    