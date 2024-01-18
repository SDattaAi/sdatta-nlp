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