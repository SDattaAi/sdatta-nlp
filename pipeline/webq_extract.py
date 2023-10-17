import requests
from bs4 import BeautifulSoup
import re

# Replace 'your_url_here' with the URL of the web page you want to scrape
url = 'https://www.palmers.at/ultra-smoothe-panties-100610465000.html'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags (img) in the HTML
    img_tags = soup.find_all('img')

    # Find all links (a tags) in the HTML
    a_tags = soup.find_all('a')

    # Define a regular expression to match JPG and PNG file extensions
    image_extensions = re.compile(r'\.(jpg|jpeg|png)')

    # Initialize a list to store image URLs
    image_urls = []

    # Extract image URLs from img tags
    for img in img_tags:
        src = img.get('src')
        if src:
            if image_extensions.search(src):
                image_urls.append(src)

    # Extract image URLs from anchor tags (links)
    for a in a_tags:
        href = a.get('href')
        if href:
            if image_extensions.search(href):
                image_urls.append(href)

    # Print the list of image URLs
    for image_url in image_urls:
        print(image_url)

else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")


