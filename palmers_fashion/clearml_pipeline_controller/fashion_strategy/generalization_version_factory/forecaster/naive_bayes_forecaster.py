from simulation.generalization_version_factory.forecaster.general_forecaster import ForecastingStrategy

class NaiveBayesForecasting(ForecastingStrategy):
    def forecast(self,dict_sales: dict, store: str, sku: str, current_date: str):
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