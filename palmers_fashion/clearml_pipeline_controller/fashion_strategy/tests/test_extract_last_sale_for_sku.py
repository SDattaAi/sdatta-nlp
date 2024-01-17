import pytest
from ... fashion_strategy.simulation.simulation_general import extract_last_sale_for_sku
store1 = 'store1'
store2 = 'store2'
sku1 = 'sku1'
sku2 = 'sku2'
current_date1 = '2024-01-19'
dict_sales1 = {'store1': {'2024-01-18': [('sku1', 5)]}}
dict_sales2 = {'store1': {'2024-01-20': [('sku1', 10)]}}
dict_sales3 = {'store2': {'2024-01-19': [('sku2', 5)]}}
dict_sales4 = {}
dict_sales5 = {'store1': {'2024-01-18': [('sku1', 5)]}}
dict_sales6 = {'store2': {'2024-01-10': [('sku2', 5641165)]}}

expected1 = 5
expected2 = None
expected3 = None
expected4 = None
expected5 = None
expected6 = 5641165
@pytest.mark.parametrize("store, sku, current_date, dict_sales, expected_result", [
    (store1, sku1, current_date1, dict_sales1, expected1),
    (store1, sku1, current_date1, dict_sales2, expected2),
    (store1, sku1, current_date1, dict_sales3, expected3),
    (store1, sku1, current_date1, dict_sales4, expected4),
    (store1, sku2, current_date1, dict_sales5, expected5),
    (store2, sku2, current_date1, dict_sales6, expected6),
])
def test_extract_last_sale_for_sku(store, sku, current_date, dict_sales, expected_result):
    result = extract_last_sale_for_sku(dict_sales, store, sku, current_date)
    assert result == expected_result
