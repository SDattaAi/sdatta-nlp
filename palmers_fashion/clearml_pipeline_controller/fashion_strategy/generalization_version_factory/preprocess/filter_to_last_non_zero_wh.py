import pandas as pd
def filter_to_last_non_zero_wh(group):
    group['date'] = pd.to_datetime(group['date'], format='%Y-%m-%d')
    last_non_zero_date = group[group['warehouse_stock'].ne(0)]['date'].max()
    day_after_last_non_zero = last_non_zero_date + pd.Timedelta(days=1)
    group = group[group['date'] <= day_after_last_non_zero]
    group["date"] = group["date"].astype(str)
    return group