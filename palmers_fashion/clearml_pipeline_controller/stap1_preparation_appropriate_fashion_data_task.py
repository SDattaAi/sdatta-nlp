
import pandas as pd
import numpy as np
import time

sales_data = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/f_sales_v_fashion.csv')
sales_data['date'] = pd.to_datetime(sales_data['date'])
sales_data['store'] = sales_data['store'].astype(str)
sales_data = sales_data.rename(columns={'total_sales':'sales'})
sales_data['sku_store'] = sales_data['sku'].astype(str) + ',' + sales_data['store'].astype(str)

mbew_fashion = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/mbew_fashion.csv')
mbew_fashion['valid_to_date'] = mbew_fashion['valid_to_date'].replace('2099-12-31', sales_data['date'].max().strftime('%Y-%m-%d'))
mbew_fashion['valid_to_date'] = pd.to_datetime(mbew_fashion['valid_to_date'])
mbew_fashion['valid_from_date'] = pd.to_datetime(mbew_fashion['valid_from_date'])
mbew_fashion['item'] = mbew_fashion['sku'].astype(str).str[:12]
mbew_fashion['sku_store'] = mbew_fashion['sku'].astype(str) + ',' + mbew_fashion['store'].astype(str)

warehouse_data = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/warehouse_stock_fashion.csv')
warehouse_data['valid_to_date'] = warehouse_data['valid_to_date'].replace('2099-12-31', sales_data['date'].max().strftime('%Y-%m-%d'))
warehouse_data['valid_from_date'] = pd.to_datetime(warehouse_data['valid_from_date'])
warehouse_data['valid_to_date'] = pd.to_datetime(warehouse_data['valid_to_date'])
warehouse_data = warehouse_data.sort_values('valid_from_date')
warehouse_data['sku_store'] = warehouse_data['sku'].astype(str) + ',' + warehouse_data['store'].astype(str)


list1 = set(warehouse_data[warehouse_data['stock'] > 0 ]['sku'].unique())
list2 = set(sales_data[(sales_data['date'] > '2019-01-01') & (sales_data['sales'] > 0)]['sku'].unique())
list_intersection = list1.intersection(list2)
relevant_skus = list(list_intersection)[:10]


sales_data = sales_data[sales_data['sku'].isin(relevant_skus)]
mbew_fashion = mbew_fashion[mbew_fashion['sku'].isin(relevant_skus)]
warehouse_data = warehouse_data[warehouse_data['sku'].isin(relevant_skus)]




start_time = time.time()
mbew_fashion = mbew_fashion.sort_values('valid_from_date')


def generate_date_ranges(row):
    return pd.date_range(row['valid_from_date'], row['valid_to_date'])

df_sales_stock_all_final = pd.DataFrame()
for store in sales_data['store'].unique():
    print("store:", store)
    unique_sku_stores = sales_data[sales_data['store'] == store]["sku_store"].unique()
    mbew_fashion['valid_from_date'] = pd.to_datetime(mbew_fashion['valid_from_date'])
    mbew_fashion['valid_to_date'] = pd.to_datetime(mbew_fashion['valid_to_date'])
    filtered_mbew_fashion = mbew_fashion[mbew_fashion['sku_store'].isin(unique_sku_stores)]
    # Function to generate date ranges

    # Apply function to create date ranges
    df_store = filtered_mbew_fashion.apply(generate_date_ranges, axis=1)
    # Create DataFrame with SKU-store and dates
    df_store = pd.DataFrame({
        'sku_store': np.repeat(filtered_mbew_fashion['sku_store'].values, df_store.str.len()),
        'date': np.concatenate(df_store.values)  # Convert DatetimeIndex to array for concatenation
    })
    # merge left by ['sku_store', 'date'] and right by ['sku_store', 'valid_to_date']
    df_store = pd.merge(df_store, filtered_mbew_fashion[['sku_store','valid_from_date', 'stock']], left_on=['sku_store', 'date'], right_on=['sku_store', 'valid_from_date'], how='left')
    # ffil stock
    df_store['stock'] = df_store['stock'].ffill()
    df_store = df_store.drop(columns=['valid_from_date'])
    df_store = pd.merge(sales_data, df_store, on=["sku_store","date"], how="right")
    df_store['sku'] = df_store['sku_store'].str.split(',').str[0]
    df_store['store'] = df_store['sku_store'].str.split(',').str[1]
    df_store['sales'] = df_store['sales'].fillna(0)
    df_store = df_store.drop(columns=['sku_store'])
    df_sales_stock_all_final = pd.concat([df_sales_stock_all_final, df_store])


df_sales_stock_all_final = df_sales_stock_all_final.sort_values(['sku', 'store', 'date'])
print("--- %s seconds ---" % (time.time() - start_time))
print("df_sales_stock_all.shape:", df_sales_stock_all_final.shape)
print("df_sales_stock_all", df_sales_stock_all_final.head())
print("df_sales_stock_all.columns:", df_sales_stock_all_final.columns)
print("df_sales_stock_all['store'].nunique():", df_sales_stock_all_final['store'].nunique())
print("df_sales_stock_all['sku'].nunique():", df_sales_stock_all_final['sku'].nunique())

start_time = time.time()

store_warehouse_id = 'VZ01'
print("store_warehouse_id:", store_warehouse_id)
warehouse_data['valid_from_date'] = pd.to_datetime(warehouse_data['valid_from_date'])
warehouse_data['valid_to_date'] = pd.to_datetime(warehouse_data['valid_to_date'])
df_warehouse_final = warehouse_data.apply(generate_date_ranges, axis=1)
df_warehouse_final = pd.DataFrame({
    'sku': np.repeat(warehouse_data['sku'].values, df_warehouse_final.str.len()),
    'date': np.concatenate(df_warehouse_final.values)  # Convert DatetimeIndex to array for concatenation
})
df_warehouse_final = pd.merge(df_warehouse_final, warehouse_data[['sku','valid_from_date', 'stock']], left_on=['sku', 'date'], right_on=['sku', 'valid_from_date'], how='left')
df_warehouse_final['stock'] = df_warehouse_final['stock'].ffill()
df_warehouse_final = df_warehouse_final.drop(columns=['valid_from_date'])



print("--- %s seconds ---" % (time.time() - start_time))
print("df_warehouse_final.shape:", df_warehouse_final.shape)
print("df_warehouse_final", df_warehouse_final.head())
print("df_warehouse_final.columns:", df_warehouse_final.columns)
print("df_warehouse_final['sku'].nunique():", df_warehouse_final['sku'].nunique())

#%%
