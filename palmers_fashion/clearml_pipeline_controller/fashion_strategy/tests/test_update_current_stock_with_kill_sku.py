import pytest
from ... fashion_strategy.simulation.simulation_general import update_current_stock_with_kill_sku

current_stock1 = {'store1': {'sku1': 5}}
end_dates1 = {'2024-01-19': ['sku1']}
date1 = '2024-01-19'
loose1 = {'sku1': 0.0}
dict_stocks1 = {'store1': {'sku1': 10}}
ashelon_stock1 = {'store1': {'2024-01-19': [('sku1', 3)]}}
expected_result1 = (
    {'store1': {}},
    {'sku1': 8.0},
    {'store1': {}}
)

current_stock2 = {'store1': {'sku1': 5}}
end_dates2 = {'2024-01-19': ['sku1']}
date2 = '2024-01-19'
loose2 = {'sku1': 0.0}
dict_stocks2 = {'store1': {'sku1': 10}}
ashelon_stock2 = {'store1': {'2024-01-20': [('sku1', 3)]}}
expected_result2 = (
    {'store1': {'sku1': 5}},
    {'sku1': 0.3},
    {'store1': {'2024-01-20': [('sku1', 3)]}}
)

current_stock3 = {'store1': {'sku1': 5}}
end_dates3 = {'2024-01-19': ['sku1']}
date3 = '2024-01-19'
loose3 = {'sku1': 0.0}
dict_stocks3 = {}
ashelon_stock3 = {}
expected_result3 = (
    {'store1': {}},
    {'sku1': 0.0},
    {}
)

@pytest.mark.parametrize("current_stock, end_dates, date, loose, dict_stocks, ashelon_stock, expected_result", [
    (current_stock1, end_dates1, date1, loose1, dict_stocks1, ashelon_stock1, expected_result1),
    (current_stock2, end_dates2, date2, loose2, dict_stocks2, ashelon_stock2, expected_result2),
    (current_stock3, end_dates3, date3, loose3, dict_stocks3, ashelon_stock3, expected_result3),
])
def test_update_current_stock_with_kill_sku(current_stock, end_dates, date, loose, dict_stocks, ashelon_stock, expected_result):
    result = update_current_stock_with_kill_sku(current_stock, end_dates, date, loose, dict_stocks, ashelon_stock)
    assert result == expected_result
