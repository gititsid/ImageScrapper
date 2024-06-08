import sys
from src.utils.common_utils import save_as_jpg
from src.get_images import ImagesFromGoogle

from src.logger import logging
from src.exception import CustomException

query_item = "Elon"
image_scrapper = ImagesFromGoogle(query_item=query_item)
urls = image_scrapper.get_image_urls()
save_as_jpg(urls=urls)
