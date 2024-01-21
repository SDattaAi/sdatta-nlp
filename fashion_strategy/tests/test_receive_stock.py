
from fashion_strategy.simulation.generalization_version_factory.utils import receive_stock
import pytest


dict_stocks1 = {'store1': {'sku1': 50}, 'store2': {'sku2': 60}, 'store3': {'sku3': 70}}
AshlonStock1 = {'store1': {'2024-01-01': [('sku1', 20)]}, 'store2': {}, 'store3': {'2024-01-01': [('sku3', 30)]}}
current_stores_arrivals_stock1 = ['store1']
date1 = '2024-01-01'
updated_stocks1 = {'store1': {'sku1': 70}, 'store2': {'sku2': 60}, 'store3': {'sku3': 70}}
updated_AshlonStock1 = {'store1': {}, 'store2': {}, 'store3': {'2024-01-01': [('sku3', 30)]}}
expected1 = (updated_stocks1, updated_AshlonStock1)
@pytest.mark.parametrize("dict_stocks, AshlonStock, current_stores_arrivals_stock, date, expected", [(dict_stocks1, AshlonStock1, current_stores_arrivals_stock1, date1, expected1)])

def test_receive_stock(dict_stocks, AshlonStock, current_stores_arrivals_stock, date, expected):
    updated_stocks, updated_AshlonStock = receive_stock(
        dict_stocks, AshlonStock, current_stores_arrivals_stock, date)
    assert expected == (updated_stocks, updated_AshlonStock)
    assert set(updated_stocks.keys()) == set(dict_stocks.keys())