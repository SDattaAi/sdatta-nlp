
from datetime import datetime


def dict_sales_from_f_sales_v(f_sales_v_fashion):
    dict_sales = {}
    for store in f_sales_v_fashion['store'].unique():
        store_data = f_sales_v_fashion[f_sales_v_fashion['store'] == store]
        dict_sales[str(store)] = {}
        for date in store_data['date'].astype(str).unique():
            date_data = store_data[store_data['date'] == date]
            dict_sales[str(store)][str(date)] = []
            for sku in date_data['sku'].unique():
                sku_data = date_data[date_data['sku'] == sku]
                amount = sku_data['sales'].sum()
                dict_sales[str(store)][str(date)].append((str(sku), amount))

    return dict_sales


def dict_stocks_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores):
    dict_stocks = {}
    for store in relevant_stores:
        if store == 'VZ01':
            dict_stocks[str(store)] = {}
            for sku in initial_stock_sku_store[initial_stock_sku_store['store'] == store]['sku'].unique():
                sku_warehouse_data = initial_stock_sku_store[
                    (initial_stock_sku_store['store'] == store) & (initial_stock_sku_store['sku'] == sku)]
                first_value_of_warehouse = sku_warehouse_data['initial_stock'].iloc[0]
                sku_warehouse_date = sku_warehouse_data['first_initial_stock_date'].iloc[0]
                other_stores_stock_after_warehouse = initial_stock_sku_store[
                    (initial_stock_sku_store['sku'] == sku) & (initial_stock_sku_store['store'] != store) & (
                                initial_stock_sku_store['first_initial_stock_date'] > sku_warehouse_date)][
                    'initial_stock'].sum()
                dict_stocks[str(store)][str(sku)] = first_value_of_warehouse - other_stores_stock_after_warehouse
        else:
            dict_stocks[str(store)] = {}
            for sku in initial_stock_sku_store[initial_stock_sku_store['store'] == store]['sku'].unique():
                dict_stocks[str(store)][str(sku)] = initial_stock_sku_store[
                    (initial_stock_sku_store['store'] == store) & (initial_stock_sku_store['sku'] == sku)][
                    'initial_stock'].iloc[0]
    return dict_stocks

def start_dates_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores):
    start_dates = {}
    for store in relevant_stores:
        store_data = initial_stock_sku_store[initial_stock_sku_store['store'] == store]
        for sku in store_data['sku'].unique():
            sku_data = store_data[store_data['sku'] == sku]
            sku_data = sku_data[sku_data['initial_stock'] != 0]
            if not sku_data.empty:
                first_date = sku_data['first_initial_stock_date'].iloc[0]
                if first_date not in start_dates:
                    start_dates[str(first_date)] = []
                start_dates[str(first_date)].append((str(sku), str(store)))
    return start_dates


def end_dates_from_f_sales_v(f_sales_v_fashion):
    end_dates = {}
    for sku in f_sales_v_fashion['sku'].unique():
        sku_data = f_sales_v_fashion[f_sales_v_fashion['sku'] == sku]
        sku_data = sku_data[sku_data['sales'] != 0]
        if not sku_data.empty:
            last_date = sku_data['date'].max().strftime('%Y-%m-%d')
            if last_date not in end_dates:
                end_dates[str(last_date)] = []
            end_dates[str(last_date)].append(str(sku))
    return end_dates



def create_fix_start_dates(start_dates, end_dates):
    # Convert string dates to datetime objects for comparison

    # Create a dictionary to map each SKU to its earliest end date
    sku_end_dates = {}
    for end_date_str, skus in end_dates.items():
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        for sku in skus:
            if sku not in sku_end_dates or end_date < sku_end_dates[sku]:
                sku_end_dates[sku] = end_date

        # Iterate through each date in start_dates and remove SKUs with earlier end dates
        for start_date_str, sku_store_pairs in list(start_dates.items()):  # Use list() to avoid RuntimeError
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

            # Iterate through each SKU-store pair
            for sku_store_pair in list(sku_store_pairs):  # Use list() to avoid RuntimeError
                sku = sku_store_pair[0]
                if sku in sku_end_dates and start_date > sku_end_dates[sku]:
                    sku_store_pairs.remove(sku_store_pair)

            # If no pairs left for the date, remove the date from start_dates
            if not sku_store_pairs:
                del start_dates[start_date_str]

        return start_dates