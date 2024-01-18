import pytest
from ... fashion_strategy.simulation.simulation_general import update_current_stock_with_kill_sku


current_stock5 = {'store1': {'sku1': 1, 'sku2': 2, 'sku3': 3}}
end_dates5 = {'2024-01-18': ['sku1', 'sku2', 'sku3']}
date5 = '2024-01-18'
loose5 = {'sku1': 0.0, 'sku2': 0.0, 'sku3': 0.0}
dict_stocks5 = {'store1': {'sku1': 10, 'sku2': 20, 'sku3': 30}}
ashelon_stock5 = {'store1': {'2024-01-18': [('sku1', 1), ('sku2', 1), ('sku3', 1)], '2024-01-19': [('sku1', 3), ('sku2', 4), ('sku3', 5)], '2024-01-20': [('sku1', 1), ('sku2', 2), ('sku3', 3)]}}
current_stock_lose_ashelon_stock5 = ({'store1': {}},
 {'sku1': 0.6, 'sku2': 0.45, 'sku3': 0.4},
 {'store1': {'2024-01-18': [], '2024-01-19': [], '2024-01-20': []}})


current_stock6 = {'store1': {'sku1': 1, 'sku2': 2, 'sku3': 3}, 'store2': {'sku1': 100, 'sku2': 200, 'sku3': 300}}
end_dates6 = {'2024-01-18': ['sku1', 'sku2']}
date6 = '2024-01-18'
loose6 = {'sku1': 0.0, 'sku2': 0.0, 'sku3': 0.0}
dict_stocks6 = {'store1': {'sku1': 10, 'sku2': 20, 'sku3': 30}, 'store2': {'sku1': 1000, 'sku2': 2000, 'sku3': 3000}}
ashelon_stock6 = {'store1': {'2024-01-18': [('sku1', 1), ('sku2', 1), ('sku3', 1)], '2024-01-19': [('sku1', 3), ('sku2', 4), ('sku3', 5)], '2024-01-20': [('sku1', 1), ('sku2', 2), ('sku3', 3)]},
                  'store2': {'2024-01-18': [('sku1', 1), ('sku2', 1), ('sku3', 1)], '2024-01-19': [('sku1', 3), ('sku2', 4), ('sku3', 5)], '2024-01-20': [('sku1', 1), ('sku2', 2), ('sku3', 3)]}}
current_stock_lose_ashelon_stock6 = ({'store1': {'sku3': 3}, 'store2': {'sku3': 300}},
                                     {'sku1': 0.1099009900990099, 'sku2': 0.10693069306930693, 'sku3': 0.0},
                                     {'store1': {'2024-01-18': [('sku3', 1)], '2024-01-19': [('sku3', 5)], '2024-01-20': [('sku3', 3)]},
                                      'store2': {'2024-01-18': [('sku3', 1)], '2024-01-19': [('sku3', 5)], '2024-01-20': [('sku3', 3)]}})
@pytest.mark.parametrize("current_stock, end_dates, date, loose, dict_stocks, ashelon_stock, expected_result", [


    (current_stock5, end_dates5, date5, loose5, dict_stocks5, ashelon_stock5, current_stock_lose_ashelon_stock5),
    (current_stock6, end_dates6, date6, loose6, dict_stocks6, ashelon_stock6, current_stock_lose_ashelon_stock6),
])
def test_update_current_stock_with_kill_sku(current_stock, end_dates, date, loose, dict_stocks, ashelon_stock, expected_result):
    result = update_current_stock_with_kill_sku(current_stock, end_dates, date, loose, dict_stocks, ashelon_stock)
    assert result == expected_result
