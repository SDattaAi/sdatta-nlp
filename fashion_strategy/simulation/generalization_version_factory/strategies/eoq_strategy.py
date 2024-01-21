from fashion_strategy.simulation.generalization_version_factory.strategies.general_strategy import GeneralStrategy
from fashion_strategy.simulation.generalization_version_factory.forecaster.eoq_forecaster import EOQForecasting
import numpy as np
class EoqStrategy(GeneralStrategy):
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, forecasting_strategy = None, **kwargs):
        super().__init__(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)
        self.forecasting_strategy = forecasting_strategy if forecasting_strategy else EOQForecasting()


    def apply_strategy(self, current_stores_replenished,sku):
        order_cost = self.kwargs.get("order_cost", 2)
        holding_cost = self.kwargs.get("holding_cost", 1)
        for store in current_stores_replenished:
            store = str(store)
            if store not in self.current_stock:
                continue
            if sku in self.current_stock[store].keys():
                if self.ActiveStores[sku][store] == 0:
                    continue
                demand = self.forecasting_strategy.forecast(self.dict_sales, store, sku, self.date)
                if demand is None:
                    continue
                eoq = ((2 * demand * order_cost) / holding_cost) ** 0.5
                potential_stock_order_from_warehouse = np.round(np.maximum(eoq - self.current_stock[store][sku], 0), 0)
                if potential_stock_order_from_warehouse > 0 and potential_stock_order_from_warehouse <= self.current_stock["VZ01"][sku]:
                    self.current_stock, self.AshlonStock, self.accumulated_stocks = self.update_AshlonStock_waerhouse(potential_stock_order_from_warehouse, sku, store)
                    print(f"apply eoq strategy for store {store} and sku {sku} with {potential_stock_order_from_warehouse} units")
        return self.current_stock, self.AshlonStock, self.accumulated_stocks