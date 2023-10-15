import requests
from bs4 import BeautifulSoup
import os

url = "https://www.basicsbypalmers.at/jaquards-badeanzug-100533747000.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'
}

response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all image tags
img_tags = soup.find_all('img')

# Downloading each image
for img in img_tags:
    img_url = img['src']
    # Handle relative URLs if needed
    if not img_url.startswith(('data:image', 'http')):
        img_url = os.path.join(url, img_url)
    print(img_url)





