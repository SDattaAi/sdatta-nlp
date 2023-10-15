import requests
from bs4 import BeautifulSoup
from lxml import html

url = 'https://www.palmers.at/smart-shirt-100549321000.html'


response = requests.get(url)
tree = html.fromstring(response.content)
element = tree.xpath('/html/body/div[2]/main/div[2]/div/div[1]/div[3]/form/div[1]/div[1]/div/div[3]')

if element:
    print(element[0].text_content())
else:
    print("Element not found.")


