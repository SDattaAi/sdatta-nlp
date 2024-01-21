

import pandas as pd
import numpy as np
import os
import pickle


def initialize_all_the_dicts(stores_simulation: list, skus_simulation: list, start_dates: dict, dict_stocks: dict) -> (
dict, dict, dict, list, list, list, list):
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
    accumulated_AshlonStock = []
    accumulated_ActiveStores = []
    start_dates_copy = start_dates.copy()
    start_dates_copy = {pd.to_datetime(date): start_dates_copy[date] for date in start_dates_copy}
    for sku in skus_simulation:
        ActiveStores[sku] = {}
    for store in stores_simulation:
        store = str(store)
        AshlonStock[store] = {}
        MissedSales[store] = {}
        ActiveStores[store] = {}
        current_stock[store] = {}
        for sku in skus_simulation:
            MissedSales[store][sku] = 0
            ActiveStores[sku][store] = 1
    return AshlonStock, MissedSales, ActiveStores, current_stock, accumulated_stocks, accumulated_AshlonStock, accumulated_ActiveStores


def initialize_kpi_structures(stores_simulation: list, skus_simulation: list) -> (dict, dict, dict, dict, dict, dict):
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
        for store in stores_simulation:
            d_wo_inv[sku][store] = 0
            d_wo_inv_wo_wh[sku][store] = 0
            Ex_i_s_r[sku][store] = {'len': 0, 'sum': 0}
            avg_integral_diff[sku][store] = {'len': 0, 'sum': 0}
            Ex_total_days_wo_inv[sku][store] = {'len': 0, 'sum': 0}

    return d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose

def update_current_stock_with_new_sku(current_stock: dict,start_dates: dict, date: str, dict_stocks: dict, Ex_total_days_wo_inv: dict, Ex_i_s_r: dict, avg_integral_diff: dict) -> tuple[dict, dict, dict, dict]:
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
        current_stock[store][sku] = dict_stocks[store][sku]
        Ex_total_days_wo_inv[sku][store] = {'len': 0, 'sum': 0}
        Ex_i_s_r[sku][store] = {'len': 0, 'sum': 0}
        avg_integral_diff[sku][store] = {'len': 0, 'sum': 0}
    return current_stock, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff


def update_current_stock_with_kill_sku(current_stock: dict, end_dates: dict, date: str, loose: dict, dict_stocks: dict,
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
    loose: dict
        loose[sku] = percent of loose
    -------
    return: current_stock, loose

    Note:
        1. loose is the percent of the stock that we have not sold
    """
    date_datetime = pd.to_datetime(date)
    for sku in end_dates[date]:
        tempo_sku_total_stock = 0
        for store in current_stock:
            if sku in current_stock[store]:
                loose[sku] += current_stock[store][sku]
                del current_stock[store][sku]
            if store in dict_stocks and sku in dict_stocks.get(store, {}):
                tempo_sku_total_stock += dict_stocks[store][sku]
            for date_str in pd.date_range(date_datetime, date_datetime + pd.Timedelta(days=2), freq="D"):
                date_str = date_str.strftime('%Y-%m-%d')
                if store in ashelon_stock and date_str in ashelon_stock.get(store, {}) and sku in ashelon_stock[
                    store].get(date_str, {}):
                    sku, amount = ashelon_stock[store][date_str]
                    loose[sku] += amount
                    del ashelon_stock[store][date_str]
        if tempo_sku_total_stock == 0:
            raise ValueError(f"initial stock for sku {sku} is 0")
        loose[sku] = loose[sku] / tempo_sku_total_stock
    return current_stock, loose, ashelon_stock


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
                    dict_stocks[store][sku] = amount
            del AshlonStock[store][date]
    return dict_stocks, AshlonStock

def update_kpi_wo_inv(d_wo_inv: dict, d_wo_inv_wo_wh: dict, current_stock: dict, Ex_total_days_wo_inv: dict) -> tuple[dict, dict, dict]:
    """
    This function update kpi dicts : d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    Args:
    --------
    d_wo_inv: dict
        d_wo_inv[sku][store] = amount
    d_wo_inv_wo_wh: dict
        d_wo_inv_wo_wh[sku][store] = amount
    current_stock: dict
        current_stock[store][sku] = amount

    -------
    return: d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    """
    for store in current_stock:
        for sku in current_stock[store]:
            if current_stock[store][sku] == 0:
                d_wo_inv[sku][store] += 1
                Ex_total_days_wo_inv[sku][store]['len'] += 1
                Ex_total_days_wo_inv[sku][store]['sum'] += d_wo_inv[sku][store]/Ex_total_days_wo_inv[sku][store]['len']
                if store != "VZ01" and current_stock[store][sku] == 0:
                    d_wo_inv_wo_wh[sku][store] += 1
            else:
                Ex_total_days_wo_inv[sku][store]['len'] += 1
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

        # del dict_sales[store][date]
    return dict_stocks, MissedSales


# %%
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


def kill_and_save_results(accumulated_stocks: dict, d_wo_inv: dict, d_wo_inv_wo_wh: dict, Ex_i_s_r: dict,
                          avg_integral_diff: dict, Ex_total_days_wo_inv: dict, loose: dict, date: str, end_dates: dict,
                          MissedSales: dict, clearml_task=None,
                          base_path: str = r'/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller_fashion',
                          simulation_name: str = 'run1', lamda: float = 0.1) -> tuple[
    dict, dict, dict, dict, dict, dict, dict, dict]:
    """
    This function kill and save results
    Args:
    --------
    d_wo_inv: dict
        d_wo_inv[sku][store] = amount
    d_wo_inv_wo_wh: dict
        d_wo_inv_wo_wh[sku][store] = amount
    Ex_i_s_r: dict
        Ex_i_s_r[sku][store] = amount
    avg_integral_diff: dict
        avg_integral_diff[sku][store] = amount
    Ex_total_days_wo_inv: dict
        Ex_total_days_wo_inv[sku][store] = amount
    loose: dict
        loose[sku] = percent of loose
    date: str
        date of the simulation
    strategy_names: str
        name of the strategy to apply
    end_dates: dict
        end_dates[date] = [(sku),...]
    MissedSales: dict
        MissedSales[store][date] = (sku, amount)
    -------
    return: d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose, MissedSales
    """
    if date not in end_dates:
        return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose, MissedSales
    final_kpi_res = {}
    simulation_dir = os.path.join(base_path, simulation_name)
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)
    for sku in end_dates[date]:
        for store in accumulated_stocks:
            if sku in accumulated_stocks[store]:
                lose = d_wo_inv[sku]["VZ01"] * (np.exp(lamda * loose[sku]) - 1), loose[sku] if store == "VZ01" else None
                avg_integral_diff_sum_divde_avg_integral_diff = avg_integral_diff[sku][store]["sum"] / \
                                                                avg_integral_diff[sku][store]["len"] if \
                avg_integral_diff[sku][store]["len"] != 0 else None
                Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv = Ex_total_days_wo_inv[sku][store]["sum"] / \
                                                                      Ex_total_days_wo_inv[sku][store]["len"] if \
                Ex_total_days_wo_inv[sku][store]["len"] != 0 else None
                Ex_i_s_r_sum_divde_Ex_i_s_r = Ex_i_s_r[sku][store]["sum"] / Ex_i_s_r[sku][store]["len"] if \
                Ex_i_s_r[sku][store]["len"] != 0 else None
                final_kpi_res[f'{sku}_{store}'] = {f'days without stock in {sku, store}: {d_wo_inv[sku][store]}',
                                                   f'days without stock in {sku, store} without warehouse: {d_wo_inv_wo_wh[sku][store]}',
                                                   f'expected value inventory sales ratio in {sku, store}: {Ex_i_s_r_sum_divde_Ex_i_s_r}',
                                                   f'average integral difference in {sku, store}: {avg_integral_diff_sum_divde_avg_integral_diff}',
                                                   f'expected value total days without inventory in {sku, store}: {Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv}',
                                                   f'loose, lose ratio in {sku} {lose}',
                                                   f'missed sales in {sku, store}: {MissedSales[store][sku]}',
                                                   f'accumulated stock in {sku, store}: {accumulated_stocks[store][sku]}'}

                # file_path = os.path.join(simulation_dir, f'{sku}_{store}.pkl')
                # with open(file_path, 'wb') as f:
                #     pickle.dump(final_kpi_res[f'{sku}_{store}'], f)
                del accumulated_stocks[store][sku], d_wo_inv[sku][store], d_wo_inv_wo_wh[sku][store], Ex_i_s_r[sku][
                    store], avg_integral_diff[sku][store], Ex_total_days_wo_inv[sku][store], MissedSales[store][sku]
        del loose[sku]
    date_ = date.replace("-", "_")
    #
    if clearml_task is None:
        file_path = os.path.join(simulation_dir, f'{date_}.pkl')
        with open(file_path, 'wb') as f:
            pickle.dump(final_kpi_res, f)
    else:
        clearml_task.upload_artifact(f'final_kpi_res_{date_}', artifact_object=final_kpi_res)

    print("final_kpi_res: ", final_kpi_res)
    return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose, MissedSales

def extract_last_sale_for_sku(dict_sales: dict,store: str,sku: str,current_date: str) :
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


def update_AshlonStock_waerhouse(potential_stock_order_from_warehouse:int,dict_stocks:dict,AshlonStock:dict, accumulated_stocks: dict,sku:str,store:str,date:str):
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
        AshlonStock[store][two_days_from_current_date_str] = AshlonStock[store].get(two_days_from_current_date_str, []) + [(sku, potential_stock_order_from_warehouse)]
        accumulated_stocks[store][sku] += potential_stock_order_from_warehouse
    return dict_stocks,AshlonStock,accumulated_stocks

def apply_strategy_naive_bayes(dict_stocks: dict, AshlonStock: dict, ActiveStores: dict, current_stores_replenished: list, dict_sales: dict, accumulated_stocks: dict, date: str,store_traveling_time_dict: dict = None) -> (dict, dict):
    """
    This function apply strategy and update dict_stocks, AshlonStock.
    The strategy is naive bayes:
    1. for every store that can be replenished from the warehouse
    2. for every sku in the store
    3. check if the store sold the last sale of the sku
    4. if the store sold the last sale of the sku
    5. add 1 to the last sale of the sku
    6. caculate the potential_stock_order_from_warehouse = amount of the last sale - the stock of the store
    7. if the potential_stock_order_from_warehouse is positive and the stock in the warehouse is enough for the order
    8. update the stock in the warehouse
    9. update the AshlonStock

    Args:
    --------
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    AshlonStock: dict
        AshlonStock[store][date] = (sku, amount)
    ActiveStores: dict
        ActiveStores[store] = 1/0
    current_stores_replenished: list
        list of stores that can be replenished from the warehouse
    dict_sales: dict
        dict_sales[store][date] = (sku, amount)
    accumulated_stocks: dict
        accumulated_stocks[store][sku] = amount
    date: str
        date of the simulation
    store_traveling_time_dict: dict
        store_traveling_time_dict[store] = traveling_time
    -------
    return: dict_stocks, AshlonStock
    """
    for store in current_stores_replenished:
        store = str(store)
        if store not in dict_stocks:
            continue
        for sku in dict_stocks[store].keys():
            if ActiveStores[sku][store] == 0:
                continue
            amount_last_sale = extract_last_sale_for_sku(dict_sales, store,sku,date) + 1 if extract_last_sale_for_sku(dict_sales, store,sku,date) is not None else None
            if amount_last_sale is None:
                continue
            potential_stock_order_from_warehouse = amount_last_sale - dict_stocks[store][sku]
            dict_stocks,AshlonStock,accumulated_stocks = update_AshlonStock_waerhouse(potential_stock_order_from_warehouse,dict_stocks,AshlonStock,accumulated_stocks,sku,store,date)
    return dict_stocks, AshlonStock, accumulated_stocks

def update_info_for_kpi(accumulated_stocks: dict,current_stock: dict, Ex_i_s_r: dict, avg_integral_diff: dict, margin_ratio: int = 3) -> tuple[dict, dict]:
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
        if store == "VZ01":
            continue
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
            avg_integral_diff[sku][store]['sum'] += current_stock[store][sku] - 1 if current_stock[store][sku] > 0 else margin_ratio
        for sku in current_stock['VZ01']:
            total_stock = np.sum([accumulated_stocks[store][sku] for store in current_stock])
            total_sales = total_stock - current_stock['VZ01'][sku]
            if total_stock == 0:
                raise ValueError(f"total initialized stock in all stores for sku {sku} is 0")
            else:
                Ex_i_s_r[sku]['VZ01']['len'] += 1
                Ex_i_s_r[sku]['VZ01']['sum'] += total_sales / total_stock
    return Ex_i_s_r, avg_integral_diff
def main_simulation(dict_deliveries_from_warehouse: dict, dict_arrivals_store_deliveries: dict, stores_simulation: list,
                    skus_simulation: list, dict_sales: dict, dict_stocks: dict, start_dates: dict, end_dates: dict,
                    task_clearml=None,
                    strategy_names: str = "naive_bayes") -> None:
    """
    This function is the main simulation function by the next steps:
    0. initialize all the dicts : AshlonStock, MissedSales, ActiveStores, current_stocks
    1. start queue
    2. Check which stores accept inventory today: 2.1 check for new sku in the store or sku to kill
                                                  2.2 check for incoming inventory
    3. receive stock and update AshlonStock
    4. update stocks by sales and update MissedSales
    5. update ActiveStores (note: update by hard data from the past from outside the simulation)
    6. current stores that can be replenished from dict_deliveries_from_warehouse
    7. apply strategy and update current_stocks, AshlonStock
    8. save results
    9. end queue

    Args:
    --------
    dict_deliveries_from_warehouse: dict
        dict_deliveries_from_warehouse[date] = [store1,store2,...]
    dict_arrivals_store_deliveries : dict
        dict_arrivals_store_deliveries[date] = [store1,store2,...]
    stores_simulation : list
        list of stores to simulate
    skus_simulation : list
        list of skus to simulate
    dict_sales : dict
        dict_sales[store][date] = (sku, amount)
    dict_stocks: dict
        dict_stocks[store][sku] = amount
    start_date : str
        start date of the simulation
    end_date : str
        end date of the simulation
    start_dates: dict
        start_dates[date] = [(sku, store),...]
    end_dates: dict
        end_dates[date] = [(sku),...]
    strategy_names: str
        name of the strategy to apply (Default: "naive_bayes")

    -------
    return: None

    Note:
        1. All constants are in the strategy
        2. The simulation is by days (every queue is a day)
        3. AshlonStock[store][date] = (sku, amount)
        4. MissedSales[store][date] = (sku, amount)
        5. ActiveStores[store] = 1/0
    """
    AshlonStock, MissedSales, ActiveStores, current_stock, accumulated_stocks, accumulated_AshlonStock, accumulated_ActiveStores = initialize_all_the_dicts(
        stores_simulation, skus_simulation, start_dates, dict_stocks)
    print("ActiveStores: ", ActiveStores)
    d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose = initialize_kpi_structures(
        stores_simulation, skus_simulation)
    start_dates_copy = start_dates.copy()
    start_dates_copy = {pd.to_datetime(date): start_dates_copy[date] for date in start_dates_copy}
    min_start_date_copy = min(start_dates_copy.keys()).strftime('%Y-%m-%d')
    dict_end_dates_copy = end_dates.copy()
    dict_end_dates_copy = {pd.to_datetime(date): dict_end_dates_copy[date] for date in dict_end_dates_copy}
    end_date = max(dict_end_dates_copy.keys()).strftime('%Y-%m-%d')
    for date in pd.date_range(min_start_date_copy, end_date, freq="D"):
        date_str = date.strftime('%Y-%m-%d')
        print(f"Processing date {date_str}")
        if date_str in start_dates.keys():
            current_stock, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff = update_current_stock_with_new_sku(
                current_stock, start_dates, date_str, dict_stocks, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff)
        if date_str in end_dates.keys():
            current_stock, loose, AshlonStock = update_current_stock_with_kill_sku(current_stock, end_dates, date_str,
                                                                                   loose, dict_stocks, AshlonStock)
        if date_str in dict_arrivals_store_deliveries:
            current_stores_arrivals_stock = dict_arrivals_store_deliveries[date_str]
            current_stock, AshlonStock = receive_stock(current_stock, AshlonStock, current_stores_arrivals_stock,
                                                       date_str)
        d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv = update_kpi_wo_inv(d_wo_inv, d_wo_inv_wo_wh, current_stock,
                                                                           Ex_total_days_wo_inv)
        current_stock, MissedSales = update_stocks_by_sales(current_stock, dict_sales, MissedSales, date_str)
        ActiveStores = update_active_stores(ActiveStores, current_stock)
        if date_str in dict_deliveries_from_warehouse:
            current_stores_replenished = dict_deliveries_from_warehouse[date_str]
            current_stock, AshlonStock, accumulated_stocks = apply_strategy_naive_bayes(current_stock, AshlonStock,
                                                                                        ActiveStores,
                                                                                        current_stores_replenished,
                                                                                        dict_sales, accumulated_stocks,
                                                                                        date_str)
        Ex_i_s_r, avg_integral_diff = update_info_for_kpi(accumulated_stocks, current_stock, Ex_i_s_r,
                                                          avg_integral_diff)
        print("date_str: ", date_str)
        accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose, MissedSales = kill_and_save_results(
            accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose,
            date_str, end_dates, MissedSales, task_clearml)