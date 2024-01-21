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