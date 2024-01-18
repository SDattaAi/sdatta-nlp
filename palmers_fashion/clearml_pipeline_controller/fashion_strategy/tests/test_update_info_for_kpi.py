import pytest
from ... fashion_strategy.simulation.simulation_general import update_info_for_kpi

# Sample input and expected output dictionaries for testing
accumulated_stocks1 = {
    'store1': {'sku1': 100, 'sku2': 200},
    'store2': {'sku1': 50, 'sku2': 150},
    'VZ01': {'sku1': 1000, 'sku2': 2000},
}
current_stock1 = {
    'store1': {'sku1': 1, 'sku2': 2},
    'store2': {'sku1': 5, 'sku2': 15},
    'VZ01': {'sku1': 10, 'sku2': 20},
}
Ex_i_s_r1 = {
    'sku1': {'store1': {'len': 2, 'sum': 0}, 'store2': {'len': 2, 'sum': 0}, 'VZ01': {'len': 8, 'sum': 0}},
    'sku2': {'store1': {'len': 2, 'sum': 0}, 'store2': {'len': 2, 'sum': 0}, 'VZ01': {'len': 10, 'sum': 0}}
}

avg_integral_diff1 = {
    'sku1': {'store1': {'len': 2, 'sum': 0}, 'store2': {'len': 2, 'sum': 0}},
    'sku2': {'store1': {'len': 2, 'sum': 0}, 'store2': {'len': 2, 'sum': 0}}
}


expected_Ex_i_s_r1 = {'sku1': {'VZ01': {'len': 11, 'sum': 2.973913043478261},
          'store1': {'len': 3, 'sum': 0.99},
          'store2': {'len': 3, 'sum': 0.9}},
 'sku2': {'VZ01': {'len': 13, 'sum': 2.974468085106383},
          'store1': {'len': 3, 'sum': 0.99},
          'store2': {'len': 3, 'sum': 0.9}}}
expected_avg_integral_diff1 = {'sku1': {'store1': {'len': 3, 'sum': 0}, 'store2': {'len': 3, 'sum': 4}},
 'sku2': {'store1': {'len': 3, 'sum': 1}, 'store2': {'len': 3, 'sum': 14}}}

@pytest.mark.parametrize(
    "accumulated_stocks, current_stock, Ex_i_s_r, avg_integral_diff, expected_Ex_i_s_r, expected_avg_integral_diff",
    [(accumulated_stocks1, current_stock1, Ex_i_s_r1, avg_integral_diff1, expected_Ex_i_s_r1, expected_avg_integral_diff1)]
)
def test_update_info_for_kpi(
    accumulated_stocks, current_stock, Ex_i_s_r, avg_integral_diff, expected_Ex_i_s_r, expected_avg_integral_diff
):
    # Call the function with the input data
    updated_Ex_i_s_r, updated_avg_integral_diff = update_info_for_kpi(
        accumulated_stocks, current_stock, Ex_i_s_r, avg_integral_diff
    )

    # Perform assertions to check if the function behaves as expected
    assert updated_Ex_i_s_r == expected_Ex_i_s_r
    assert updated_avg_integral_diff == expected_avg_integral_diff
