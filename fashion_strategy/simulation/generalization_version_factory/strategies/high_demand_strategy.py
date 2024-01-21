from simulation.generalization_version_factory.strategies.general_strategy import GeneralStrategy
from simulation.generalization_version_factory.forecaster.high_demand_forecaster import HighDemandForecasting
# from datetime import datetime, timedelta
import numpy as np
from collections import Counter
class HighDemandStrategy(GeneralStrategy):
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date,
                 store_weights=None,  forecasting_strategy = None, **kwargs):
        super().__init__(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)
        self.store_weights = store_weights if store_weights is not None else {}
        self.forecasting_strategy = forecasting_strategy if forecasting_strategy else HighDemandForecasting()

    def apply_strategy(self, current_stores_replenished,sku):
        if sku not in self.current_stock.get("VZ01", {}):
            return self.current_stock, self.AshlonStock, self.accumulated_stocks
        if self.current_stock.get("VZ01", {})[sku] <= 0:
            return self.current_stock, self.AshlonStock, self.accumulated_stocks

        vz01_stock = self.current_stock.get("VZ01", {})

        current_stores_replenished_ = [str(store) for store in current_stores_replenished]
        stores_sorted_by_stock = sorted(
            [store for store in self.current_stock.keys() if store in current_stores_replenished_],
            key=lambda store: self.current_stock[store].get(sku, 0),
            reverse=True)
        for store in stores_sorted_by_stock:
            if store == "VZ01" or store not in stores_sorted_by_stock:
                continue
            if self.ActiveStores[sku].get(store, 0) == 0:
                continue
            if sku not in self.accumulated_stocks[store]:
                continue
            store_weight, base_allocation_amount = self.forecasting_strategy.forecast(self.dict_sales, store, sku, self.date,self.store_weights)
            potential_stock_order_from_warehouse = max(np.ceil(min(vz01_stock[sku], base_allocation_amount * store_weight)),
                                                                0)
            self.current_stock, self.AshlonStock, self.accumulated_stocks = self.update_AshlonStock_waerhouse(
                potential_stock_order_from_warehouse, sku, store)
            print(f"apply high demand strategy for store {store} and sku {sku} with {potential_stock_order_from_warehouse} units")
        return self.current_stock,self.AshlonStock,self.accumulated_stocks