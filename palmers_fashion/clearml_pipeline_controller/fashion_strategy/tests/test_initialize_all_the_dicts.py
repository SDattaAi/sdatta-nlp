
from ... fashion_strategy.generalization_version_factory.utils_ import initialize_all_the_dicts
import pytest

skus_simulation1 = ['sku1', 'sku2']
dict_stocks1 = {'store1': {'sku1': 50, 'sku2': 30}, 'store2': {'sku1': 60, 'sku2': 20}}
AshlonStock1 = {'store1': {}, 'store2': {}}
MissedSales1 = {'store1': {'sku1': 0, 'sku2': 0}, 'store2': {'sku1': 0, 'sku2': 0}}
ActiveStores1 = {'sku1': {'store1': 1, 'store2': 1}, 'sku2': {'store1': 1, 'store2': 1}}
current_stock1 = {'store1': {}, 'store2': {}}
accumulated_stocks1 = {'store1': {'sku1': 50, 'sku2': 30}, 'store2': {'sku1': 60, 'sku2': 20}}

expected_outputs = (AshlonStock1, MissedSales1, ActiveStores1, current_stock1, accumulated_stocks1)
@pytest.mark.parametrize("skus_simulation, dict_stocks, expected_outputs", [(skus_simulation1, dict_stocks1, expected_outputs)])

def test_initialize_all_the_dicts(skus_simulation, dict_stocks, expected_outputs):
    AshlonStock, MissedSales, ActiveStores, current_stock, \
        accumulated_stocks = initialize_all_the_dicts(skus_simulation, dict_stocks)
    assert expected_outputs == (AshlonStock, MissedSales, ActiveStores, current_stock, accumulated_stocks)
    assert set(AshlonStock.keys()) == {'store1', 'store2'}
    assert set(MissedSales.keys()) == {'store1', 'store2'}
    assert set(current_stock.keys()) == {'store1', 'store2'}
    assert set(accumulated_stocks.keys()) == {'store1', 'store2'}
    assert set(ActiveStores.keys()) == {'sku1', 'sku2'}




