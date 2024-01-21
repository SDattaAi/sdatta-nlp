import pickle
from clearml import Task
import json
import pandas as pd
def load_dummy_data_for_check(task_id:str):
    step2_task = Task.get_task(task_id=task_id)
    step2_task_artifacts = step2_task.artifacts
    dict_deliveries_from_warehouse_path = step2_task_artifacts['dict_deliveries_from_warehouse'].get_local_copy()
    with open(dict_deliveries_from_warehouse_path, 'r') as f:
        dict_deliveries_from_warehouse = json.load(f)
    dict_arrivals_store_deliveries_path = step2_task_artifacts['dict_arrivals_store_deliveries'].get_local_copy()
    with open(dict_arrivals_store_deliveries_path, 'r') as f:
        dict_arrivals_store_deliveries = json.load(f)
    skus_simulation_path = step2_task_artifacts['skus_simulation'].get_local_copy()
    with open(skus_simulation_path, 'rb') as f:
        skus_simulation = pickle.load(f)
    print("skus_simulation: ", skus_simulation)
    dict_sales_path = step2_task_artifacts['dict_sales'].get_local_copy()
    with open(dict_sales_path, 'rb') as f:
        dict_sales = pickle.load(f)
    dict_stocks_path = step2_task_artifacts['dict_stocks'].get_local_copy()
    with open(dict_stocks_path, 'r') as f:
        dict_stocks = json.load(f)
    start_dates_path = step2_task_artifacts['start_dates'].get_local_copy()
    with open(start_dates_path, 'r') as f:
        start_dates = json.load(f)
    end_dates_path = step2_task_artifacts['end_dates'].get_local_copy()
    with open(end_dates_path, 'r') as f:
        end_dates = json.load(f)
    return dict_deliveries_from_warehouse,dict_arrivals_store_deliveries,skus_simulation,dict_sales,dict_stocks,start_dates,end_dates

def fix_deliveries_dict(fix_dict_arrivals_stors:dict, dict_arrivals_store_deliveries:dict,dict_deliveries_from_wharehouse_dict:dict):
    for date,stores in dict_arrivals_store_deliveries.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    for date,stores in dict_deliveries_from_wharehouse_dict.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    return dict_arrivals_store_deliveries,dict_deliveries_from_wharehouse_dict


#%%
def initialize_stocks(df_stock_sales, df_warehouse, stores, skus):
    dict_stocks = {store: {sku: 0 for sku in skus} for store in stores + ["VZ01"]}
    store_stock = df_stock_sales.groupby(['store', 'sku']).apply(lambda x: x[x['stock'] > 0]['stock'].iloc[0] if not x[x['stock'] > 0].empty else 0)
    for (store, sku), stock in store_stock.items():
        dict_stocks[store][sku] = stock
    dict_sum_sku_stock = {sku: sum(dict_stocks[store][sku] for store in stores) for sku in skus}
    for sku in skus:
        warehouse_stock = df_warehouse[df_warehouse['sku'] == sku]['warehouse_stock'].max()
        dict_stocks["VZ01"][sku] = max(warehouse_stock - dict_sum_sku_stock.get(sku, 0), 0)  # Prevent negative stock
    return dict_stocks

#%%
def create_dict_sales(df_stock_sales):
    filtered_df = df_stock_sales[df_stock_sales['sales'] != 0]
    grouped_df = filtered_df.groupby(['store', 'date', 'sku'])['sales'].sum().reset_index()
    grouped_df['date'] = grouped_df['date'].dt.strftime('%Y-%m-%d')
    dict_sales = {}
    for _, row in grouped_df.iterrows():
        store = row['store']
        date = row['date']
        sku = row['sku']
        amount = row['sales']
        if store not in dict_sales:
            dict_sales[store] = {}
        if date not in dict_sales[store]:
            dict_sales[store][date] = []
        dict_sales[store][date].append((sku, amount))
    return dict_sales

def sku_simulations(df_stock):
    skus_simulation = df_stock["sku"].unique().tolist()
    return skus_simulation


# %%
def filter_from_first_non_zero(group):
    first_non_zero_index = group[group['stock_palmers'].ne(0)].index.min()
    return group.loc[first_non_zero_index:]


# %%
def filter_to_last_non_zero(group):
    group['date'] = pd.to_datetime(group['date'], format='%Y-%m-%d')
    last_non_zero_date = group[group['stock_palmers'].ne(0)]['date'].max()
    day_after_last_non_zero = last_non_zero_date + pd.Timedelta(days=1)
    group = group[group['date'] <= day_after_last_non_zero]
    group["date"] = group["date"].astype(str)
    return group


# %%
def filter_from_first_non_zero_warehouse(group):
    first_non_zero_index = group[group['warehouse_stock'].ne(0)].index.min()
    return group.loc[first_non_zero_index:]


# %%
def filter_to_last_non_zero_wh(group):
    group['date'] = pd.to_datetime(group['date'], format='%Y-%m-%d')
    last_non_zero_date = group[group['warehouse_stock'].ne(0)]['date'].max()
    day_after_last_non_zero = last_non_zero_date + pd.Timedelta(days=1)
    group = group[group['date'] <= day_after_last_non_zero]
    group["date"] = group["date"].astype(str)
    return group


# %%
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
