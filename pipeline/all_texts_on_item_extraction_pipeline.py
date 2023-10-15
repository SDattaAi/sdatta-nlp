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
print(artikelstamm_df.head())

