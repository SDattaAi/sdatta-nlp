from vision_and_nlp_models.utils import translate_to_english, get_from_url_palmers
import pandas as pd

item = '100549321000'
url = 'https://www.palmers.at/smart-shirt-' + item + '.html'
title, description, materials = get_from_url_palmers(url)
text_to_translate = title + " " + description + "\n" + materials
translated_text = translate_to_english(text_to_translate)
print(f"Original Text: {text_to_translate}")
print(f"Translated Text(en): {translated_text}")

artikelstamm_df = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/l_artikelstamm.csv', sep=';')

#print all columns
pd.set_option('display.max_columns', None)
rows_with_item = artikelstamm_df[artikelstamm_df['sammelartikel'] == str(item)]
desc_from_artikelstamm = rows_with_item['wgrbez_en'].values[0]
colors = rows_with_item['color'].unique()
sizes = rows_with_item['size'].unique()

print(f"Description from Artikelstamm: {desc_from_artikelstamm}")
print(f"Colors: {colors}")
print(f"Sizes: {sizes}")

