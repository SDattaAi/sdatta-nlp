
from notebooks.oran.feature_engineering.google_trend.functions import *
def item_description_preparation_pipeline(df):
    df['item'] = df['sammelartikel_nachfolger']
    df = df[df[['wgrbez_de','wgrbez_en','item']].notnull().all(axis=1)]
    df = item_description_fix_tokens(df, 'wgrbez_de')
    df = item_description_fix_tokens(df, 'wgrbez_en')
    df = item_description_fix_tokens(df, 'description')
    df["full_desc_en"] = df["wgrbez_en"] + " " + df["description"]
    df["full_desc_en"] = df["full_desc_en"].str.replace('\d+', '')
    df["full_desc_en"] = df["full_desc_en"].str.replace(r'\b\w\b', '').str.replace('\s+', ' ', regex=True)
    return df[['item', 'description', 'wgrbez_de', 'wgrbez_en', "full_desc_en"]]