from simulation.generalization_version_factory.utils.initialize_all_the_dicts import initialize_all_the_dicts
from simulation.generalization_version_factory.utils.initialize_kpi_structures import initialize_kpi_structures
from simulation.generalization_version_factory.utils.update_current_stock_with_new_sku import update_current_stock_with_new_sku
from simulation.generalization_version_factory.utils.update_current_stock_with_kill_sku import update_current_stock_with_kill_sku
from simulation.generalization_version_factory.utils.receive_stock import receive_stock
from simulation.generalization_version_factory.utils.update_kpi_wo_inv import update_kpi_wo_inv
from simulation.generalization_version_factory.utils.update_stocks_by_sales import update_stocks_by_sales
from simulation.generalization_version_factory.utils.update_active_stores import update_active_stores
from simulation.generalization_version_factory.utils.update_info_for_kpi import update_info_for_kpi
from simulation.generalization_version_factory.utils.kill_and_save_results import kill_and_save_results
from simulation.generalization_version_factory.strategy_selector.strategy_selector import StrategySelector
from simulation.generalization_version_factory.forecaster.forecast_factory.forecast_factory import ForecastFactory
from simulation.generalization_version_factory.strategies.strategies_factory.strategies_factory import StrategyFactory
import pandas as pd



def main_simulation(dict_deliveries_from_warehouse: dict, dict_arrivals_store_deliveries: dict, skus_simulation: list,
                    dict_sales: dict, dict_stocks: dict, start_dates: dict, end_dates: dict, original_strategy_key,original_forecast_key,
                    use_strategy_selector=False,strategy_key_high_demand=None,forecast_key_high_demand=None, **strategy_specific_args) -> None:
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
    forecast_factory = ForecastFactory()
    forecast = forecast_factory.get_forecast(original_forecast_key)
    strategy_specific_args['forecast'] = forecast
    strategy_factory = StrategyFactory()
    AshlonStock, MissedSales, ActiveStores, current_stock, accumulated_stocks = initialize_all_the_dicts(
        skus_simulation, dict_stocks)
    d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose = initialize_kpi_structures(
        dict_stocks, skus_simulation)
    start_dates_copy = start_dates.copy()
    start_dates_copy = {pd.to_datetime(date): start_dates_copy[date] for date in start_dates_copy}
    min_start_date_copy = min(start_dates_copy.keys()).strftime('%Y-%m-%d')
    dict_end_dates_copy = end_dates.copy()
    dict_end_dates_copy = {pd.to_datetime(date): dict_end_dates_copy[date] for date in dict_end_dates_copy}
    end_date = max(dict_end_dates_copy.keys()).strftime('%Y-%m-%d')
    all_results = {}
    for date in pd.date_range(min_start_date_copy, end_date, freq="D"):
        date_str = date.strftime('%Y-%m-%d')
        print(f"Processing date {date_str}")
        if date_str in start_dates.keys():
            current_stock, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff = update_current_stock_with_new_sku(
                current_stock, start_dates, date_str, dict_stocks, Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff)
        if date_str in end_dates.keys():
            current_stock, loose, AshlonStock = update_current_stock_with_kill_sku(current_stock, end_dates, date_str,
                                                                                   loose, accumulated_stocks,
                                                                                   AshlonStock)
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

            for sku in skus_simulation:
                if use_strategy_selector:
                    original_strategy_class = strategy_factory.strategy_mapping.get(original_strategy_key)
                    high_demand_strategy_class = strategy_factory.strategy_mapping.get(strategy_key_high_demand)

                    strategy_selector = StrategySelector(original_strategy_class, high_demand_strategy_class,
                                                         **strategy_specific_args)
                    selected_strategy_class, selected_strategy_args = strategy_selector.select_strategy(sku,
                                                                                                        current_stock)
                    if selected_strategy_class.__name__ == original_strategy_key:
                        strategy = strategy_factory.get_strategy(original_strategy_key, current_stock, AshlonStock, ActiveStores,
                                                                 dict_sales, accumulated_stocks, date_str,
                                                                 **strategy_specific_args)
                        current_stock, AshlonStock, accumulated_stocks = strategy.apply_strategy(
                            current_stores_replenished, sku)
                    else:
                        forecast = forecast_factory.get_forecast(forecast_key_high_demand)
                        strategy_specific_args['forecast'] = forecast
                        strategy = strategy_factory.get_strategy(strategy_key_high_demand, current_stock, AshlonStock,
                                                                 ActiveStores, dict_sales, accumulated_stocks,
                                                                 date_str, **strategy_specific_args)
                        current_stock, AshlonStock, accumulated_stocks = strategy.apply_strategy(
                            current_stores_replenished, sku)

                else:
                    strategy = strategy_factory.get_strategy(original_strategy_key, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date_str, **strategy_specific_args)
                    current_stock, AshlonStock, accumulated_stocks = strategy.apply_strategy(current_stores_replenished, sku)

        Ex_i_s_r, avg_integral_diff = update_info_for_kpi(accumulated_stocks, current_stock, Ex_i_s_r,
                                                              avg_integral_diff)
        accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose, MissedSales, final_kpi_res = \
            kill_and_save_results(
                accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose,
                date_str, end_dates, MissedSales)
        all_results[date_str] = final_kpi_res
    return all_results