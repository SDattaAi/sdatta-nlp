from fashion_strategy.simulation.generalization_version_factory.forecaster.general_forecaster import ForecastingStrategy

class EOQForecasting(ForecastingStrategy):
    def forecast(self,dict_sales, store, sku, date):
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
        if store in dict_sales and date in dict_sales[store]:
            demand = sum(amount for sale_sku, amount in dict_sales[store][date] if sale_sku == sku)
            return demand
        else:
            return None