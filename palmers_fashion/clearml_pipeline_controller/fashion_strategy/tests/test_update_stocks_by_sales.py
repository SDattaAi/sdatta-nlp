
from ... fashion_strategy.generalization_version_factory.utils_ import update_stocks_by_sales
import pytest

dict_stocks1 = {'store1': {'sku1': 70}, 'store2': {'sku1': 60}}
dict_sales1 = {'store1': {'2024-01-02': [('sku1', 30)]}, 'store2': {'2024-01-02': [('sku1', 70)]}}
MissedSales1 = {'store1': {'sku1': 0}, 'store2': {'sku1': 0}}
date1 = '2024-01-02'
updated_stocks1 = {'store1': {'sku1': 40}, 'store2': {'sku1': 0}}
updated_missed_sales1 = {'store1': {'sku1': 0}, 'store2': {'sku1': 10}}
expected1 = (updated_stocks1, updated_missed_sales1)

# for sku, amount in dict_sales[store][date]:
#dict_stocks[store][sku] >= amount
@pytest.mark.parametrize("dict_stocks, dict_sales, MissedSales, date, expected", [(dict_stocks1, dict_sales1, MissedSales1, date1, expected1)])

def test_update_stocks_by_sales(dict_stocks, dict_sales, MissedSales, date, expected):
    updated_stocks, updated_missed_sales = update_stocks_by_sales(dict_stocks, dict_sales, MissedSales, date)
    assert updated_stocks == expected[0]
    assert updated_missed_sales == expected[1]
