from bs4 import BeautifulSoup
import requests

# Your URL
url = 'https://www.palmers.at/smart-shirt-100549321000.html'
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')

# Find the td element with class 'col data' and attribute data-th="Material"
material_data = soup.find('td', {'class': 'col data', 'data-th': 'Material'})

# Print the text content of the td element
if material_data:
    print(material_data.text)
else:
    print("Element not found with the given attributes.")

