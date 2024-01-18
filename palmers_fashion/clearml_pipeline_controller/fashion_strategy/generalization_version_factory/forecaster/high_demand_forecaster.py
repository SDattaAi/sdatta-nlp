from simulation.generalization_version_factory.forecaster.general_forecaster import ForecastingStrategy
from datetime import datetime, timedelta
import numpy as np
from collections import Counter

class HighDemandForecasting(ForecastingStrategy):
    def forecast(self,dict_sales, store, sku, date, store_weights):
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