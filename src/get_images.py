import sys
import requests

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

from src.utils.common_utils import save_as_jpg, push_to_mongodb
from src.logger import logging
from src.exception import CustomException

class ImagesFromGoogle:
    def __init__(self, query_item: str) -> None:
        self.query_item = query_item
        self.base_url = f"https://www.google.com/search?q={self.query_item}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M"
    
    def get_image_urls(self, save_images=False, save_in_mongodb=True) -> list[dict]:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        query_url = self.base_url

        urlclient = requests.get(query_url)
        image_page = urlclient.content

        image_page_html = bs(image_page , "html.parser")

        image_tags = image_page_html.find_all("img")
        image_tags = image_tags[1:]

        urls = []
        for i, image_tag in enumerate(image_tags):
            image_url =  image_tag['src']
            url = {f"{self.query_item}_{i}": image_url}
            urls.append(url)

        if save_images:
            save_as_jpg(urls=urls)

        if save_in_mongodb:
            push_to_mongodb(urls)
            
        return urls
    

if __name__ == "__main__":
    query_item = "abc"
    image_scrapper = ImagesFromGoogle(query_item=query_item)

    urls = image_scrapper.get_image_urls(save_images=True, save_in_mongodb=True)
