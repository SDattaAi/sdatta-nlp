def receive_stock(dict_stocks: dict, AshlonStock: dict, current_stores_arrivals_stock: list, date: str) -> (dict, dict):
    """
    This function receive stock and update AshlonStock for the current stores that arrive stock today .
    description:
    1. update dict_stocks by the stock that arrive today
    2. update AshlonStock by the stock that arrive today
    3. delete the date from AshlonStock
     Args:
    --------
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    AshlonStock: dict
        AshlonStock[store][date] = (sku, amount)
    current_stores_arrivals_stock: list
        list of stores that arrive stock today
    date: str
        date of the simulation
    -------
    return: dict_stocks, AshlonStock
    """
    for store in current_stores_arrivals_stock:
        store = str(store)
        if store not in dict_stocks:
            continue
        if date not in AshlonStock[store]:
            continue

        if date in AshlonStock[store]:
            for delivery in AshlonStock[store][date]:
                sku, amount = delivery
                if sku in dict_stocks[store]:
                    dict_stocks[store][sku] += amount
                else:
                    continue
            del AshlonStock[store][date]
    return dict_stocks, AshlonStock