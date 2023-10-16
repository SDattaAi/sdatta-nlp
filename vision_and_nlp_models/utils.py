
import torch
from torchvision.transforms import ToPILImage
from googletrans import Translator
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
from io import BytesIO


def extract_image_urls(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)

    browser.get(url)
    browser.implicitly_wait(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

    style_tags = soup.find_all(style=re.compile("background-image"))
    for tag in style_tags:
        match = re.search(r'url\(["\']?(.*?)["\']?\)', tag['style'])
        if match:
            img_urls.append(match.group(1))
    browser.quit()
    return img_urls


def take_relevant_images_from_url(url, item):
    images = extract_image_urls(url)
    images = [img for img in images if item in img]
    images = [img for img in images if img.endswith('.jpg') or img.endswith('.png') or img.endswith('.jpeg') or img.endswith('.webp')]

    image_dict = {}

    for url in images:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        area = width * height

        filename = url.split('/')[-1]

        # Check if the filename already exists in the dictionary.
        # If it does, compare the areas and keep the URL with the larger image.
        if filename in image_dict:
            existing_area, _ = image_dict[filename]
            if area > existing_area:
                image_dict[filename] = (area, url)
        else:
            image_dict[filename] = (area, url)
    return image_dict

def get_from_url_palmers(url):
    title = None
    description = None
    materials = None
    # Send a GET request to the URL to fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div element with class "value" and itemprop "description"
        div_element_desc = soup.find('div', class_='value', itemprop='description')
        div_element_title = soup.find('h1', class_='page-title', itemprop='name')
        material_data = soup.find('td', {'class': 'col data', 'data-th': 'Material'})

        # Check if the description div element was found
        if div_element_desc:
            # Extract the text value from the div element
            description = div_element_desc.text.strip()


        # Check if the title h1 element was found
        if div_element_title:
            # Extract the text value from the h1 element
            title = div_element_title.text.strip()

        if material_data:
            # Extract the text value from the h1 element
            materials = material_data.text.strip()

    else:
        print("Failed to fetch webpage. Status code:", response.status_code)


    return title, description, materials

def is_english(text):
    # You can use a language detection library here, like langdetect,
    # to check if the text is in English.
    # For simplicity, we'll assume it's English if it contains only ASCII characters.
    return all(ord(char) < 128 for char in text)

def translate_to_english(text):
    if is_english(text):
        return text  # Return the original text if it's already in English

    translator = Translator()
    translated_text = translator.translate(text, dest="en")
    return translated_text.text
def fix_channels(t):
    """
    Some images may have 4 channels (transparent images) or just 1 channel (black and white images), in order to let the images have only 3 channels. I am going to remove the fourth channel in transparent images and stack the single channel in back and white images.
    :param t: Tensor-like image
    :return: Tensor-like image with three channels
    """
    if len(t.shape) == 2:
        return ToPILImage()(torch.stack([t for i in (0, 0, 0)]))
    if t.shape[0] == 4:
        return ToPILImage()(t[:3])
    if t.shape[0] == 1:
        return ToPILImage()(torch.stack([t[0] for i in (0, 0, 0)]))
    return ToPILImage()(t)