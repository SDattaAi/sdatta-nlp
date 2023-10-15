from vision_and_nlp_models.utils import translate_to_english, get_from_url_palmers
import pandas as pd
from googlesearch import search
import warnings
from sdatta_learn.loader.load_from_postgres import get_stock_between_dates_and_stores
warnings.filterwarnings("ignore")
import json
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

print(stock_df)
for item in fashion_items['item'].unique()[:5]:
    print("item", item)
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
    if url is not  None:
      title, description, materials = get_from_url_palmers(url)
    text_to_translate = ''
    if title is not None:
        text_to_translate = text_to_translate + title + " "
    if description is not None:
        text_to_translate = text_to_translate + description + " "
    if materials is not None:
        text_to_translate = text_to_translate + materials + " "
    translated_text = translate_to_english(text_to_translate)
    print(f"Translated Text(en): {translated_text}")
    #print all columns
    pd.set_option('display.max_columns', None)
    rows_with_item = artikelstamm_df[artikelstamm_df['sammelartikel'] == str(item)]
    desc_from_artikelstamm = rows_with_item['wgrbez_en'].values[0]
    colors = rows_with_item['color'].unique()
    sizes = rows_with_item['size'].unique()

    print(f"Description from Artikelstamm: {desc_from_artikelstamm}")
    print(f"Colors: {colors}")
    print(f"Sizes: {sizes}")

