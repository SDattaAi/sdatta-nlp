from vision_and_nlp_models.utils import translate_to_english, get_from_url_palmers
import pandas as pd
from googlesearch import search
import warnings
warnings.filterwarnings("ignore")

fashion_items = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/fashion_items.csv').drop('Unnamed: 0', axis=1)
artikelstamm_df = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/l_artikelstamm.csv', sep=';')
stock_df = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/stock_14052023.csv')
print(stock_df.columns)
stock_df['item'] = stock_df['sku'].astype(str).str[0:12]
stock_df_items = stock_df[(stock_df['to_date'] == '2099-12-31') & (stock_df['stock'].astype(int) > 0)]['item'].unique()
print("stock_df_items" , stock_df_items)
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

