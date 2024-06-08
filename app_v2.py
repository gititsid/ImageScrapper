import requests
from PIL import Image
import streamlit as st

from src.utils.common_utils import save_as_jpg, push_to_mongodb
from src.get_images import ImagesFromGoogle

from src.logger import logging
from src.exception import CustomException

# Page layout
st.set_page_config(
    page_title="Images from Google",
    page_icon="🔍",
    layout="wide"
)

# User interface
st.header("Images from Google!")

# User inputs
st.sidebar.subheader('User Inputs:')
search_item = st.sidebar.text_input('What/Who are you looking for?')
search_item = search_item.replace(' ', '') if ' ' in search_item else search_item

if search_item: 
    image_scrapper = ImagesFromGoogle(search_item)
    urls = image_scrapper.get_image_urls(save_images=False, save_in_mongodb=False)

    images = []
    for url in urls:
        image = Image.open(requests.get(list(url.values())[0], stream=True).raw)
        image = image.resize((140, 140))
        images.append(image)

    # All Images
    st.subheader(f'Found these images for {search_item}:')
    st.image(images[:18])
