from simulation.generalization_version_factory.strategies.general_strategy import GeneralStrategy

class OptSwAvgStrategy(GeneralStrategy):
    def __init__(self, current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs):
        super().__init__(current_stock, AshlonStock, ActiveStores, dict_sales, accumulated_stocks, date, **kwargs)
    def apply_strategy(self, current_stores_replenished,sku):
        sw_data = self.kwargs.get("sw_data", None)
        duration = self.kwargs.get("duration", None)
        for store in current_stores_replenished:
            store = str(store)
            if store not in self.current_stock:
                continue
            if sku in self.current_stock[store].keys():
                if self.ActiveStores[sku][store] == 0:
                    continue
                key = str(sku) + "," + str(store)
                if key not in sw_data:
                    continue
                if self.date in sw_data[key]:
                    potential_order = duration * (sw_data[key][self.date] - 1) - self.current_stock[store][sku] + 1
                else:
                    continue
                if potential_order > 0 and potential_order <= self.current_stock["VZ01"][sku]:
                    self.current_stock, self.AshlonStock, self.accumulated_stocks = self.update_AshlonStock_waerhouse(potential_order, sku, store)
        return self.current_stock, self.AshlonStock, self.accumulated_stocks, self.store_weights