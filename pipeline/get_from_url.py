import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage
url = 'https://www.palmers.at/urban-nights-pyjama-100639031000.html'
def get_from_url_palmers(url):
    try:
        # Send a GET request to the URL to fetch the webpage content
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div element with class "value" and itemprop "description"
            div_element_desc = soup.find('div', class_='value', itemprop='description')
            div_element_title = soup.find('h1', class_='page-title', itemprop='name')

            # Check if the description div element was found
            if div_element_desc:
                # Extract the text value from the div element
                description = div_element_desc.text.strip()
                print("Description:", description)
            else:
                print("Description element not found.")

            # Check if the title h1 element was found
            if div_element_title:
                # Extract the text value from the h1 element
                title = div_element_title.text.strip()
                print("Title:", title)
            else:
                print("Title element not found.")
        else:
            print("Failed to fetch webpage. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", str(e))


    return title, description
