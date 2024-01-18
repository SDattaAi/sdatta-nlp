def update_AshlonStock_waerhouse(potential_stock_order_from_warehouse: int, dict_stocks: dict, AshlonStock: dict,
                                 accumulated_stocks: dict, sku: str, store: str, date: str):
    """
    This function update the AshlonStock and dict_stocks by the following description:
    1. check if the potential_stock_order_from_warehouse is positive and the stock in the warehouse is enough for the order
    2. update the stock in the warehouse
    3. update the AshlonStock for the future date (2 days from the current date)
    Args:
    --------
    potential_stock_order_from_warehouse: int
        amount of the last sale - the stock of the store
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    AshlonStock: dict
        AshlonStock[store][date] = (sku, amount)
    accumulated_stocks: dict
        accumulated_stocks[store][sku] = amount
    sku: str
        sku id
    store: str
        store id
    date: str
        date of the simulation
    -------
    return: dict_stocks, AshlonStock
    """
    if potential_stock_order_from_warehouse <= dict_stocks["VZ01"][sku] and potential_stock_order_from_warehouse > 0:
        store = str(store)
        dict_stocks["VZ01"][sku] -= potential_stock_order_from_warehouse
        two_days_from_current_date = pd.to_datetime(date) + pd.Timedelta(days=2)
        two_days_from_current_date_str = two_days_from_current_date.strftime('%Y-%m-%d')
        AshlonStock[store][two_days_from_current_date_str] = AshlonStock[store].get(two_days_from_current_date_str,
                                                                                    []) + [
                                                                 (sku, potential_stock_order_from_warehouse)]
        accumulated_stocks[store][sku] += potential_stock_order_from_warehouse
    return dict_stocks, AshlonStock, accumulated_stocks