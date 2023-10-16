from vision_and_nlp_models.utils import take_relevant_images_from_url
import requests
from PIL import Image
from io import BytesIO
import os


url = 'https://www.basicsbypalmers.at/jaquards-badeanzug-100533747000.html'
item = '100533747000'
image_dict = take_relevant_images_from_url(url, item)
# add folder path /Users/guybasson/Desktop/sdatta-nlp/photos/palmers/100549321000 if not exist
if not os.path.exists('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + item):
    os.makedirs('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + item)
# delete all files in folder
for filename in os.listdir('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + item):
    file_path = os.path.join('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + item, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# download the images in the dictionary /Users/guybasson/Desktop/sdatta-nlp/photos/palmers/100549321000
for (area, url) in image_dict.values():
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    filename = url.split('/')[-1]
    img.save('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + item + '/' + filename)
    print(f"URL: {url}")
    print(f"Dimensions: {width} x {height}")
    print("----------------------")
