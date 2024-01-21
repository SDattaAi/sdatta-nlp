from datetime import datetime


def validate_stock_zero_for_warehouse(dict_stocks, warehouse_store='VZ01'):
    list_sku_to_delete = []
    bool = True
    if warehouse_store in dict_stocks:
        for sku, stock in dict_stocks[warehouse_store].items():
            if stock == 0:
                list_sku_to_delete.append(sku)
                bool = False
    return bool


def validate_start_end_dates(start_dates, end_dates):
    for date, sku_store_pairs in start_dates.items():
        start_date = datetime.strptime(date, '%Y-%m-%d')
        for sku, store in sku_store_pairs:
            end_date_str = next((d for d in end_dates if sku in end_dates[d]), None)
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                if start_date > end_date:
                    return False
    return True


def validate_store_sku_identifiers(dict_stocks, dict_sales):
    valid_stores = set(dict_stocks.keys())
    valid_skus = {sku for store_skus in dict_stocks.values() for sku in store_skus.keys()}
    for store, sales_data in dict_sales.items():
        if store not in valid_stores:
            return False
        for date, sales in sales_data.items():
            for sku, _ in sales:
                if sku not in valid_skus:
                    return False
    return True


def validate_sales_date_format(dict_sales):
    for store, sales_data in dict_sales.items():
        for date in sales_data.keys():
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return False
    return True


def validate_sku_availability(dict_stocks, dict_sales):
    for store, sales_data in dict_sales.items():
        for date, sales in sales_data.items():
            for sku, _ in sales:
                if not any(sku in stock_dict and stock_dict[sku] > 0 for stock_dict in dict_stocks.values()):
                    return False
    return True


def validate_sales_dates_within_simulation_period(dict_sales, start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    for store, sales_data in dict_sales.items():
        for date in sales_data:
            current_date = datetime.strptime(date, '%Y-%m-%d')
            if current_date < start or current_date > end:
                return False
    return True


def validate_non_empty_inputs(dict_stocks, dict_sales):
    return bool(dict_stocks) and bool(dict_sales)


def validate_warehouse_delivery_dates_and_stores(dict_deliveries_from_warehouse):
    for date, stores in dict_deliveries_from_warehouse.items():
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False  # Invalid date format
    return True


def validate_store_delivery_dates_and_stores(dict_arrivals_store_deliveries):
    for date, stores in dict_arrivals_store_deliveries.items():
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False  # Invalid date format
    return True


def validate_non_empty_deliveries(dict_deliveries_from_warehouse, dict_arrivals_store_deliveries):
    return bool(dict_deliveries_from_warehouse) and bool(dict_arrivals_store_deliveries)


def validate_stock_not_negative_for_warehouse(dict_stocks, warehouse_store='VZ01'):
    list_sku_to_delete = []
    bool = True
    if warehouse_store in dict_stocks:
        for sku, stock in dict_stocks[warehouse_store].items():
            if stock <= 0:
                list_sku_to_delete.append(sku)
                bool = False
    return bool, list_sku_to_delete


def validate_positive_stocks(dict_stocks):
    negative_warehouse_stocks = []
    bool = True
    for store, skus in dict_stocks.items():
        if any(stock < 0 for stock in skus.values()):
            negative_warehouse_stocks.append(store)
            bool = False
    return bool



