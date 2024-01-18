def update_stocks_by_sales(dict_stocks: dict, dict_sales: dict, MissedSales: dict, date: str) -> (dict, dict):
    """
    This function update stocks by sales and update MissedSales by the following description:
        1. check if the stock is enough for the sales
        2. if the stock is enough for the sales update the stock
        3. if the stock is not enough for the sales update the MissedSales
    Args:
    --------
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    dict_sales: dict
        dict_sales[store][date] = (sku, amount)
    MissedSales: dict
        MissedSales[store][date] = (sku, amount)
    -------
    return: dict_stocks, MissedSales
    """
    for store in dict_sales:
        store = str(store)
        if store not in dict_stocks:
            continue
        if date not in dict_sales[store]:
            continue
        for sale in dict_sales[store][date]:
            sku, amount = sale
            if sku not in dict_stocks[store]:
                continue
            if dict_stocks[store][sku] >= amount:
                dict_stocks[store][sku] -= amount
            else:
                MissedSales[store][sku] += amount - dict_stocks[store][sku]
                dict_stocks[store][sku] = 0
    return dict_stocks, MissedSales