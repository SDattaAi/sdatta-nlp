from simulation.generalization_version_factory.strategies.general_strategy import GeneralStrategy
from simulation.generalization_version_factory.forecaster.jit_forecaster import JITForecasting
import numpy as np
from datetime import datetime, timedelta
import pandas as pd


class JitStrategy(GeneralStrategy):
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date,
                 store_traveling_time_dict=None, forecasting_strategy = None, **kwargs):
        super().__init__(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)
        self.store_traveling_time_dict = store_traveling_time_dict if store_traveling_time_dict is not None else {}
        self.forecasting_strategy = forecasting_strategy if forecasting_strategy else JITForecasting()


    @staticmethod
    def calculate_jit_order_amount(current_stock, sku, store, demand_forecast, stock_needed_by_date, date):
        current_stock_level = current_stock[store].get(sku, 0)
        days_until_needed = (datetime.strptime(stock_needed_by_date, "%Y-%m-%d") - pd.to_datetime(date)).days
        daily_demand_forecast = demand_forecast / 6
        required_stock = daily_demand_forecast * days_until_needed
        order_amount = max(required_stock - current_stock_level, 0)
        return order_amount

    def apply_strategy(self, current_stores_replenished, sku):
        past_dates = [(datetime.strptime(self.date, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d") for i in
                      range(6)]
        for store in current_stores_replenished:
            store = str(store)
            if store not in self.current_stock or store == "VZ01":
                continue
            if sku in self.current_stock[store].keys():
                if self.ActiveStores[sku][store] == 0:
                    continue
                demand_forecast = self.forecasting_strategy.forecast(self.dict_sales, store, sku, past_dates)
                lead_time = self.store_traveling_time_dict.get(store, 1)
                stock_needed_by_date = (datetime.strptime(self.date, "%Y-%m-%d") + timedelta(days=lead_time)).strftime(
                    "%Y-%m-%d")
                if demand_forecast is None:
                    continue
                potential_stock_order = np.ceil(
                    self.calculate_jit_order_amount(self.current_stock, sku, store, demand_forecast,
                                                    stock_needed_by_date, self.date))
                if potential_stock_order > 0 and potential_stock_order <= self.current_stock["VZ01"][sku]:
                    self.current_stock, self.AshlonStock, self.accumulated_stocks = self.update_AshlonStock_waerhouse(
                        potential_stock_order, sku, store)
        return self.current_stock, self.AshlonStock, self.accumulated_stocks
