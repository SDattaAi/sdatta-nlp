import pandas as pd
def update_current_stock_with_kill_sku(current_stock: dict, end_dates: dict, date: str, lose: dict, dict_stocks: dict,
                                       ashelon_stock: dict) -> tuple[dict, dict, dict]:
    """
    This function update current_stock with kill sku
    Args:
    --------
    current_stock: dict
        current_stock[store][sku] = amount
    end_dates: dict
        end_dates[date] = [(sku),...]
    date: str
        date of the simulation
    lose: dict
        lose[sku] = percent of lose
    -------
    return: current_stock, lose

    Note:
        1. lose is the percent of the stock that we have not sold
    """
    date_datetime = pd.to_datetime(date)
    for sku in end_dates[date]:
        tempo_sku_total_stock = 0
        for store in current_stock:
            if sku in current_stock[store]:
                lose[sku] += current_stock[store][sku]
                del current_stock[store][sku]
            if store in dict_stocks and sku in dict_stocks.get(store, {}):
                tempo_sku_total_stock += dict_stocks[store][sku]
            for date_str in pd.date_range(date_datetime, date_datetime + pd.Timedelta(days=2), freq="D"):

                date_str = date_str.strftime('%Y-%m-%d')

                if store in ashelon_stock and date_str in ashelon_stock.get(store, {}) and sku in [item[0] for item in ashelon_stock[
                    store].get(date_str, {})]:
                    # find the index of sku
                    sku_index = [item[0] for item in ashelon_stock[store].get(date_str, {})].index(sku)

                    sku, amount = ashelon_stock[store][date_str][sku_index]
                    lose[sku] += amount

                    del ashelon_stock[store][date_str][sku_index]
        if tempo_sku_total_stock == 0:
            raise ValueError(f"initial stock for sku {sku} is 0")
        lose[sku] = lose[sku] / tempo_sku_total_stock
    return current_stock, lose, ashelon_stock