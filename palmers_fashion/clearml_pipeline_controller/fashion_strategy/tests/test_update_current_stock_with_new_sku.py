import pytest
from ... fashion_strategy.generalization_version_factory.utils_ import update_current_stock_with_new_sku

current_stock1 = {'store1': {'sku1': 5}}
start_dates1 = {'2024-01-19': [('sku1', 'store1')]}
date1 = '2024-01-19'
dict_stocks1 = {'store1': {'sku1': 10}}
expected_result1 = ({'store1': {'sku1': 10}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}})

current_stock2 = {'store1':{}}
start_dates2 = {'2024-01-19': [('sku1', 'store1')]}
date2 = '2024-01-19'
dict_stocks2 = {'store1': {'sku1': 10}}
expected_result2 = ({'store1': {'sku1': 10}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}})

current_stock3 = {'store3': {'sku1': 5}}
start_dates3 = {'2024-01-19':[]}
date3 = '2024-01-19'
dict_stocks3 = {'store3':{'sku1': 1000}, 'store1': {'sku1': 10}}
expected_result3 = ({'store3': {'sku1': 5}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}})

current_stock4 = {'store1': {'sku1': 5}}
start_dates4 = {'2024-01-19': [('sku1', 'store1')]}
date4 = '2024-01-19'
dict_stocks4 = {'store2':{}, 'store1': {}}
expected_result4 = ({'store1': {'sku1': 0}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}}, {'sku1': {'store1': {'len': 0, 'sum': 0}}})

@pytest.mark.parametrize("current_stock, start_dates, date, dict_stocks, expected_result", [
    (current_stock1, start_dates1, date1, dict_stocks1, expected_result1),
    (current_stock2, start_dates2, date2, dict_stocks2, expected_result2),
    (current_stock3, start_dates3, date3, dict_stocks3, expected_result3),
    (current_stock4, start_dates4, date4, dict_stocks4, expected_result4),
])
def test_update_current_stock_with_new_sku(current_stock, start_dates, date, dict_stocks, expected_result):
    Ex_total_days_wo_inv = {'sku1': {'store1': {'len': 0, 'sum': 0}}}
    Ex_i_s_r = {'sku1': {'store1': {'len': 0, 'sum': 0}}}
    avg_integral_diff = {'sku1': {'store1': {'len': 0, 'sum': 0}}}

    result = update_current_stock_with_new_sku(current_stock, start_dates, date, dict_stocks,
                                               Ex_total_days_wo_inv, Ex_i_s_r, avg_integral_diff)
    assert result == expected_result

#