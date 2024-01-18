from typing import Optional
from datetime import datetime, timedelta
import numpy as np
from collections import Counter


class Forecaster:
    @staticmethod
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

    @staticmethod
    def extract_demand_forecast_for_sku_for_jit(dict_sales, store, sku, past_dates):
        total_sales = 0
        count = 0
        for past_date in past_dates:
            if past_date in dict_sales.get(store, {}):
                sales_on_date = dict_sales[store][past_date]
                for sale_entry in sales_on_date:
                    if sale_entry[0] == sku:
                        total_sales += sale_entry[1]
                        count += 1
            else:
                pass
        if count == 0:
            return None
        return total_sales / count

    @staticmethod
    def extract_demand_for_sku_for_eoq(dict_sales, store, sku, date):
        if store in dict_sales and date in dict_sales[store]:
            demand = sum(amount for sale_sku, amount in dict_sales[store][date] if sale_sku == sku)
            return demand
        else:
            return None

    @staticmethod
    def forecast_high_demand_for_sku(dict_sales, store, sku, date, store_weights):
        MAX_STORE_WEIGHT = 8
        past_dates = [(datetime.strptime(date, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        sales_history = [dict_sales[store][past_date] for past_date in past_dates if past_date in dict_sales[store]]
        sales_counter = Counter(sale[0] for sales_on_date in sales_history for sale in sales_on_date)
        sales_velocity = sales_counter[sku] / 30
        time_window = max(7, int(sales_velocity * 7))
        adjusted_sales_history = sales_history[-time_window:]
        total_sales = np.sum(
            [float(sale[1]) for sales_on_date in adjusted_sales_history for sale in
             sales_on_date]) if adjusted_sales_history else 1
        sales_performance = sum(
            [1 for sales_on_date in adjusted_sales_history for sale in sales_on_date if sale[0] == sku]) / (
                                    total_sales + 1e-7)
        store_weight = (store_weights.get(store, 0) + sales_performance) / 2
        store_weight = min(store_weight, MAX_STORE_WEIGHT)
        store_weights[store] = store_weight
        base_allocation_per_store = 1
        base_allocation_amount = base_allocation_per_store * sales_performance
        return store_weight, base_allocation_amount
