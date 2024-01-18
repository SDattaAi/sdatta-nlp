from simulation.generalization_version_factory.forecaster.general_forecaster import ForecastingStrategy

class JITForecasting(ForecastingStrategy):
    def forecast(self,dict_sales, store, sku, past_dates):
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