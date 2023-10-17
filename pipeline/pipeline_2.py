from PIL import Image
from transformers import YolosFeatureExtractor, YolosForObjectDetection
from torchvision.transforms import ToTensor
from vision_and_nlp_models.yolo_utils import *
from vision_and_nlp_models.utils import fix_channels
from transformers import CLIPProcessor, CLIPModel
from vision_and_nlp_models.clip_utils import clip_results
import json
import warnings
warnings.filterwarnings("ignore")
from vision_and_nlp_models.utils import translate_to_english, get_from_url_palmers
import pandas as pd
from googlesearch import search
import warnings
from sdatta_learn.loader.load_from_postgres import get_stock_between_dates_and_stores
warnings.filterwarnings("ignore")
import json
from vision_and_nlp_models.utils import take_relevant_images_from_url
import requests
from PIL import Image
from io import BytesIO
import os
fashion_items = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/fashion_items.csv').drop('Unnamed: 0', axis=1)
artikelstamm_df = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/l_artikelstamm.csv', sep=';')
with open(
        "/Users/guybasson/PycharmProjects/sdatta_packages_new/palmers_tasks/models_base_stock_tasks/outputs_folder/preparation_config_dict.json",
        "r") as f:
    preparation_config_dict = json.load(f)
sales_filled_table = preparation_config_dict["sales_filled_table_name"]
item_status_table = preparation_config_dict["sorting_bonnet_table_name"]
pg_host = preparation_config_dict["pg_host"]
pg_port = preparation_config_dict["pg_port"]
pg_user = preparation_config_dict["pg_user"]
pg_password = preparation_config_dict["pg_password"]
pg_database = preparation_config_dict["pg_database"]
stock_df = get_stock_between_dates_and_stores(pg_host, pg_port, pg_user, pg_password, pg_database, pd.to_datetime('15-10-2023'),
                                             "'100' , '57'")
stock_df['item'] = stock_df['matnr'].astype(str).str[3:15]
stock_df['valid_to_date'] = pd.to_datetime(stock_df['valid_to_date'])
stock_df_items = stock_df[(stock_df['valid_to_date'] == '2099-12-31') & (stock_df['lbkum'] > 0)]['item'].unique()
fashion_items['item'] = fashion_items['sku'].astype(str).str[0:12]
fashion_items = fashion_items[(fashion_items['item'].isin(artikelstamm_df['sammelartikel'].unique())) &
                              (fashion_items['item'].isin(stock_df_items))]
print("number of items:", fashion_items['item'].nunique())
items_no_url = []
len_items = len(fashion_items['item'].unique())
df_of_items_info = pd.DataFrame()
i = 0
for item in fashion_items['item'].unique():
    i = i + 1
    print(i, "/", len_items)
    print("item", item)
    rows_with_item = artikelstamm_df[artikelstamm_df['sammelartikel'] == str(item)]
    desc_from_artikelstamm = rows_with_item['wgrbez_en'].values[0]
    colors_from_artikelstamm = rows_with_item['color'].unique()
    sizes_from_artikelstamm = rows_with_item['size'].unique()

    query = str(item) + " palmers"
    for url in search(query, num_results=5):
        if ("palmers" in url) and (str(item) in url):
            break
        else:
            url = None
    print("final url", url)
    title = ""
    description = ""
    materials = ""
    if url is not None:
        title, description, materials = get_from_url_palmers(url)
        title_from_internet_en = title
        description_from_internet_en = description
        materials_from_internet_en = materials
    if title is not None:
        title_from_internet_en = translate_to_english(title)
    if description is not None:
        description_from_internet_en = translate_to_english(description)
    if materials is not None:
        materials_from_internet_en = translate_to_english(materials)

    item_photos = []
    ## check  /Users/guybasson/Desktop/sdatta-nlp/photos/palmers/ + item exist
    if os.path.exists('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + str(item)):
        item_photos =  os.listdir('/Users/guybasson/Desktop/sdatta-nlp/photos/palmers/' + str(item))
        print(item_photos)

    df_of_items_info = df_of_items_info.append({'item': item,
                                                'title_from_internet_en': title_from_internet_en,
                                                'desc_from_artikelstamm': desc_from_artikelstamm,
                                                'colors_from_artikelstamm': colors_from_artikelstamm,
                                                'sizes_from_artikelstamm': sizes_from_artikelstamm,
                                                'description_from_internet_en': description_from_internet_en,
                                                'materials_from_internet_en': materials_from_internet_en}, ignore_index=True)


print(df_of_items_info)

