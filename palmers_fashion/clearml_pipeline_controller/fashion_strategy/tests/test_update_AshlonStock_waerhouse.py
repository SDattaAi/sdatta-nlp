import pytest
from ... fashion_strategy.generalization_version_factory.utils_ import update_AshlonStock_waerhouse

sku = 'sku1'
store = 'store1'
date = '2024-01-03'

accumulated_stocks1 = {
    'store1': {'sku1': 20, 'sku2': 25},
    'store2': {'sku1': 25, 'sku2': 30},
}
potential_order1 = 5
dict_stocks1 = {'VZ01': {'sku1': 10}}
AshlonStock1 = {
    'store1': {'2024-01-01': [('sku1', 5)], '2024-01-02': [('sku2', 10)]},
    'store2': {'2024-01-01': [('sku1', 8)], '2024-01-02': [('sku2', 12)]},
}

dict_stocks_expected1 = {'VZ01': {'sku1': 5}}
AshlonStock_expected1 = {'store1': {'2024-01-01': [('sku1', 5)], '2024-01-02': [('sku2', 10)], '2024-01-05': [('sku1', 5)]},
                'store2': {'2024-01-01': [('sku1', 8)], '2024-01-02': [('sku2', 12)]}}
accumulated_stocks_expected1 = {'store1': {'sku1': 25, 'sku2': 25}, 'store2': {'sku1': 25, 'sku2': 30}}
expected1 = (dict_stocks_expected1, AshlonStock_expected1, accumulated_stocks_expected1)

@pytest.mark.parametrize("potential_order, dict_stocks, AshlonStock, accumulated_stocks, sku, store, date, expected",
                         [(potential_order1, dict_stocks1, AshlonStock1, accumulated_stocks1, sku, store, date, expected1)

                          ])
def test_update_AshlonStock_waerhouse(potential_order, dict_stocks, AshlonStock, accumulated_stocks, sku, store, date, expected):
    dict_stocks, AshlonStock, accumulated_stocks = update_AshlonStock_waerhouse(potential_order, dict_stocks,
                                                                                AshlonStock, accumulated_stocks, sku,
                                                                                store, date)


    assert dict_stocks == expected[0]
    assert AshlonStock == expected[1]
    assert accumulated_stocks == expected[2]
