def initialize_all_the_dicts(skus_simulation: list, dict_stocks: dict) -> (
        dict, dict, dict,dict, dict):
    """
    This function initialize all the dicts : AshlonStock, MissedSales, ActiveStores, current_stocks
    Args:
    --------
    stores_simulation : list
        list of stores to simulate
    skus_simulation : list
        list of skus to simulate
    start_dates: dict
        start_dates[date] = [(sku, store),...]

    -------
    return:  AshlonStock, MissedSales, ActiveStores
    """
    AshlonStock = {}
    MissedSales = {}
    ActiveStores = {}
    current_stock = {}
    accumulated_stocks = dict_stocks.copy()
    for sku in skus_simulation:
        ActiveStores[sku] = {}
    for store in dict_stocks:
        store = str(store)
        AshlonStock[store] = {}
        MissedSales[store] = {}
        current_stock[store] = {}
        for sku in skus_simulation:
            MissedSales[store][sku] = 0
            ActiveStores[sku][store] = 1
    return AshlonStock, MissedSales, ActiveStores, current_stock, accumulated_stocks