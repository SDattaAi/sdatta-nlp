import pandas as pd
def creat_dict_end_dates(df_palmers):
    """
    dic_end_dates[date] = [sku1, sku2, ...]
    """
    dict_end_dates = {}
    df_palmers["date"] = pd.to_datetime(df_palmers["date"])
    for sku, group in df_palmers.groupby(['sku']):
        last_sale_date = group[group['sales'].ne(0)]['date'].max()
        if pd.notna(last_sale_date):
            end_date = (last_sale_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            dict_end_dates.setdefault(end_date, []).append(sku)
    return dict_end_dates