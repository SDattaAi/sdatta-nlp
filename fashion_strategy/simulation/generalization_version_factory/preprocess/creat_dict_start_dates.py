from fashion_strategy.simulation.generalization_version_factory.preprocess.filter_from_first_non_zero import filter_from_first_non_zero
from fashion_strategy.simulation.generalization_version_factory.preprocess.filter_from_first_non_zero_warehouse import filter_from_first_non_zero_warehouse
def creat_dict_start_dates(df_palmers, df_warehouse):
    """
    dic_start_dates[date] = [(sku, store),...]
    """
    dict_start_dates = {}
    df_palmers["date"] = df_palmers["date"].astype(str)
    df_palmers = df_palmers.rename(columns={"stock": "stock_palmers"})
    df_palmers = df_palmers[["stock_palmers", "store", "sku", "date", "sales"]]
    df_warehouse_grouped = df_warehouse.groupby(['sku'])
    unique_groups = df_palmers.groupby(['store', 'sku'])
    for (store, sku), group in unique_groups:
        filtered_group_start = filter_from_first_non_zero(group)
        if not filtered_group_start.empty:
            start_date = filtered_group_start['date'].min()
            if start_date not in dict_start_dates:
                dict_start_dates[start_date] = []
            dict_start_dates[start_date].append((sku, store))
    for sku in df_warehouse_grouped:
        filtered_group_start = filter_from_first_non_zero_warehouse(sku[1])
        if not filtered_group_start.empty:
            start_date = filtered_group_start['date'].min()
            start_date = start_date.strftime('%Y-%m-%d')
            if start_date not in dict_start_dates:
                dict_start_dates[start_date] = []
            dict_start_dates[start_date].append((sku[0], "VZ01"))
    return dict_start_dates