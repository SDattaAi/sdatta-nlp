from typing import Optional
import numpy as np
import pandas as pd

def extract_last_sale_for_sku(dict_sales: dict, store: str, sku: str, current_date: str) -> Optional[int]:
    """
    This function extract the last date and sku from dict_sales
    Args:
    --------
    dict_sales: dict
        dict_sales[store][date] = (sku, amount)
    store: str
        store id
    -------
    return: last_date, sku
    """
    if store not in dict_sales:
        return None
    for date in dict_sales[store].keys():
        if current_date <= date:
            continue
        for sale in dict_sales[store][date]:
            sale_sku, amount = sale
            if sale_sku == sku:
                return amount
    return None

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


def initialize_kpi_structures(dict_stocks: dict, skus_simulation: list) -> (dict, dict, dict, dict, dict, dict):
    """
    This function initialize all the kpi dicts : d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv
    Args:
    --------
    stores_simulation : list
        list of stores to simulate
    skus_simulation : list
        list of skus to simulate

    -------
    return:  d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv
    """
    d_wo_inv = {}
    d_wo_inv_wo_wh = {}
    Ex_i_s_r = {}
    avg_integral_diff = {}
    Ex_total_days_wo_inv = {}
    loose = {}
    for sku in skus_simulation:
        d_wo_inv[sku] = {}
        d_wo_inv_wo_wh[sku] = {}
        Ex_i_s_r[sku] = {}
        avg_integral_diff[sku] = {}
        Ex_total_days_wo_inv[sku] = {}
        loose[sku] = 0
        for store in dict_stocks:
            d_wo_inv[sku][store] = 0
            d_wo_inv_wo_wh[sku][store] = 0
            Ex_i_s_r[sku][store] = {'len': 0, 'sum': 0}
            avg_integral_diff[sku][store] = {'len': 0, 'sum': 0}
            Ex_total_days_wo_inv[sku][store] = {'len': 0, 'sum': 0}

    return d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose


def kill_and_save_results(accumulated_stocks: dict, d_wo_inv: dict, d_wo_inv_wo_wh: dict, Ex_i_s_r: dict,
                          avg_integral_diff: dict, Ex_total_days_wo_inv: dict, lose: dict, date: str, end_dates: dict,
                          MissedSales: dict, lamda: float = 0.1):
    """
    This function processes and calculates KPIs, and returns updated dictionaries along with final_kpi_res.

    Args:
    --------
    accumulated_stocks: dict
        Dictionary of accumulated stocks.
    d_wo_inv: dict
        Dictionary of days without inventory.
    d_wo_inv_wo_wh: dict
        Dictionary of days without inventory without warehouse.
    Ex_i_s_r: dict
        Dictionary of expected value of inventory sales ratio.
    avg_integral_diff: dict
        Dictionary of average integral differences.
    Ex_total_days_wo_inv: dict
        Dictionary of expected value of total days without inventory.
    lose: dict
        Dictionary of lose percentages.
    date: str
        Date of the simulation.
    end_dates: dict
        Dictionary of end dates.
    MissedSales: dict
        Dictionary of missed sales.
    lamda: float, optional
        Lambda value (default is 0.1).

    Returns:
    -------
    Tuple containing accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff,
    Ex_total_days_wo_inv, lose, MissedSales, final_kpi_res.
    """
    if date not in end_dates:
        return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, lose, MissedSales, {}
    final_kpi_res = {}
    for sku in end_dates[date]:
        for store in accumulated_stocks:
            if sku in accumulated_stocks[store]:
                lose_value_per_sku = d_wo_inv[sku]["VZ01"] * (np.exp(lamda * lose[sku]) - 1), lose[sku] if store == "VZ01" else None
                avg_integral_diff_sum_divde_avg_integral_diff = avg_integral_diff[sku][store]["sum"] / \
                                                                avg_integral_diff[sku][store]["len"] if \
                avg_integral_diff[sku][store]["len"] != 0 else None
                Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv = Ex_total_days_wo_inv[sku][store]["sum"] / \
                                                                      Ex_total_days_wo_inv[sku][store]["len"] if \
                Ex_total_days_wo_inv[sku][store]["len"] != 0 else None
                Ex_i_s_r_sum_divde_Ex_i_s_r = Ex_i_s_r[sku][store]["sum"] / Ex_i_s_r[sku][store]["len"] if \
                Ex_i_s_r[sku][store]["len"] != 0 else None
                final_kpi_res[f'{sku}_{store}'] = {f'days without stock': d_wo_inv[sku][store],
                                                   f'days without stock, without warehouse': d_wo_inv_wo_wh[sku][store],
                                                   f'expected value inventory sales ratio': Ex_i_s_r_sum_divde_Ex_i_s_r,
                                                   f'average integral difference': avg_integral_diff_sum_divde_avg_integral_diff,
                                                   f'expected value total days without inventory': Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv,
                                                   f'lose ratio': lose_value_per_sku,
                                                   f'missed sales': MissedSales[store][sku],
                                                   f'accumulated stock': accumulated_stocks[store][sku]}
            if sku in accumulated_stocks[store]:
                del accumulated_stocks[store][sku]
                del MissedSales[store][sku]
        del lose[sku], Ex_total_days_wo_inv[sku], Ex_i_s_r[sku], d_wo_inv_wo_wh[sku], d_wo_inv[sku], avg_integral_diff[
            sku]
    return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, lose, MissedSales, final_kpi_res


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


def update_active_stores(ActiveStores: dict, dict_stocks: dict) -> dict:
    """
    This function update ActiveStores (note: update by hard data from the past from outside the simulation)


    assumption for now: all the stores are active
    for later: we will need to decide which stores are active and which are not by timeline interval rule
    Args:
    --------
    ActiveStores: dict
        ActiveStores[store] = 1/0
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    -------
    return: ActiveStores
    """
    return ActiveStores



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

def update_info_for_kpi(accumulated_stocks: dict, current_stock: dict, Ex_i_s_r: dict, avg_integral_diff: dict,
                        margin_ratio: int = 3) -> tuple[dict, dict]:
    """
    This function update kpi dicts : Ex_i_s_r, avg_integral_diff
    Args:
    --------
    accumulated_stocks: dict
        accumulated_stocks[store][sku] = amount
    current_stock: dict
        current_stock[store][sku] = amount

    -------
    return: Ex_i_s_r, avg_integral_diff
    """
    for store in current_stock:
        total_stock, total_sales = 0, 0
        if store != "VZ01":
            for sku in current_stock[store]:
                total_stock += accumulated_stocks[store][sku]
                total_sales += accumulated_stocks[store][sku] - current_stock[store][sku]
                if total_stock == 0:
                    Ex_i_s_r[sku][store]['len'] += 1
                    Ex_i_s_r[sku][store]['sum'] += 0
                else:
                    Ex_i_s_r[sku][store]['len'] += 1
                    Ex_i_s_r[sku][store]['sum'] += total_sales / total_stock
                avg_integral_diff[sku][store]['len'] += 1
                avg_integral_diff[sku][store]['sum'] += current_stock[store][sku] - 1 if current_stock[store][sku] > 0 \
                    else margin_ratio
        for sku in current_stock['VZ01']:
            relevant_store_per_sku = [store for store in current_stock if sku in current_stock[store]]
            total_stock = np.sum([accumulated_stocks[store][sku] for store in relevant_store_per_sku])
            total_sales = total_stock - current_stock['VZ01'][sku]
            if total_stock == 0:
                print(f"total initialized stock in all stores for sku {sku} is 0")
            else:
                Ex_i_s_r[sku]['VZ01']['len'] += 1
                Ex_i_s_r[sku]['VZ01']['sum'] += total_sales / total_stock
    return Ex_i_s_r, avg_integral_diff

def update_kpi_wo_inv(d_wo_inv: dict, d_wo_inv_wo_wh: dict, current_stock: dict, Ex_total_days_wo_inv: dict) -> tuple[
    dict, dict, dict]:
    """
    This function update kpi dicts : d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    Args:
    --------
    d_wo_inv: dict
        d_wo_inv[sku][store] = amount
    d_wo_inv_wo_wh: dict
        d_wo_inv_wo_wh[sku]['VZ01'] = amount
    current_stock: dict
        current_stock[store][sku] = amount

    -------
    return: d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    """
    for store in current_stock:
        for sku in current_stock[store]:
            Ex_total_days_wo_inv[sku][store]['len'] += 1
            if current_stock[store][sku] == 0:
                d_wo_inv[sku][store] += 1
                Ex_total_days_wo_inv[sku][store]['sum'] += 1
                if store != "VZ01":
                    d_wo_inv_wo_wh[sku][store] += 1
    return d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv


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