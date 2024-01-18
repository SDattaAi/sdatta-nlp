from abc import ABC, abstractmethod
import pandas as pd
class GeneralStrategy:
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs):
        self.current_stock = current_stock
        self.AshlonStock = AshlonStock
        self.ActiveStores = ActiveStores
        self.dict_sales = dict_sales
        self.accumulated_stocks = accumulated_stocks
        self.date = date
        self.kwargs = kwargs

    @abstractmethod
    def apply_strategy(self, *args, **kwargs):
        pass

    def update_AshlonStock_waerhouse(self, potential_stock_order_from_warehouse, sku, store):
        if potential_stock_order_from_warehouse <= self.current_stock["VZ01"][
            sku] and potential_stock_order_from_warehouse > 0:
            store = str(store)
            self.current_stock["VZ01"][sku] -= potential_stock_order_from_warehouse
            two_days_from_current_date = pd.to_datetime(self.date) + pd.Timedelta(days=2)
            two_days_from_current_date_str = two_days_from_current_date.strftime('%Y-%m-%d')
            self.AshlonStock[store][two_days_from_current_date_str] = self.AshlonStock[store].get(
                two_days_from_current_date_str, []) + [(sku, potential_stock_order_from_warehouse)]
            self.accumulated_stocks[store][sku] += potential_stock_order_from_warehouse
        return self.current_stock, self.AshlonStock, self.accumulated_stocks

