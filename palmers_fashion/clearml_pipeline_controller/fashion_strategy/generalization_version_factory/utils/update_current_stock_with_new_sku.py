def update_current_stock_with_new_sku(current_stock: dict, start_dates: dict, date: str, dict_stocks: dict,
                                      Ex_total_days_wo_inv: dict, Ex_i_s_r: dict, avg_integral_diff: dict) -> tuple[
    dict, dict, dict, dict]:
    """
    This function update current_stock with new sku
    Args:
    --------
    current_stock: dict
        current_stock[store][sku] = amount
    start_dates: dict
        start_dates[date] = [(sku, store),...]
    date: str
        date of the simulation
    -------
    return: current_stock, Ex_tottal_days_wo_inv, Ex_i_s_r, avg_integral_diff
    """
    for data in start_dates[date]:
        sku, store = data
        current_stock[store][sku] = dict_stocks[store].get(sku, 0)
        Ex_total_days_wo_inv[sku][store] = {'len': 0, 'sum': 0}
        Ex_i_s_r[sku][store] = {'len': 0, 'sum': 0}
        avg_integral_diff[sku][store] = {'len': 0, 'sum': 0}
    return current_stock, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff