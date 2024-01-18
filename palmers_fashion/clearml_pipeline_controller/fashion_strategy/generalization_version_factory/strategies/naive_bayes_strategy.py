from simulation.generalization_version_factory.strategies.general_strategy import GeneralStrategy
from simulation.generalization_version_factory.forecaster.naive_bayes_forecaster import NaiveBayesForecasting

class NaiveBayesStrategy(GeneralStrategy):
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, forecasting_strategy = None, **kwargs):
        super().__init__(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)
        self.forecasting_strategy = forecasting_strategy if forecasting_strategy else NaiveBayesForecasting()

    def apply_strategy(self, current_stores_replenished,sku):
        for store in current_stores_replenished:
            store = str(store)
            if store not in self.current_stock:
                continue
            if sku in self.current_stock[store].keys():
                if self.ActiveStores[sku][store] == 0:
                    continue
                amount_last_sale = self.forecasting_strategy.forecast(self.dict_sales, store, sku, self.date) + 1 if self.forecasting_strategy.forecast(self.dict_sales, store, sku, self.date) is not None else None
                if amount_last_sale is None:
                    continue
                potential_stock_order_from_warehouse = amount_last_sale - self.current_stock[store][sku]
                self.current_stock, self.AshlonStock, self.accumulated_stocks = self.update_AshlonStock_waerhouse(potential_stock_order_from_warehouse, sku, store)
        return self.current_stock,self.AshlonStock,self.accumulated_stocks