import pytest
from ... fashion_strategy.simulation.simulation_general import update_kpi_wo_inv

# Sample input and expected output dictionaries for testing
d_wo_inv1 = {'sku1': {'store1': 0, 'store2': 1}, 'sku2': {'store1': 0, 'store2': 0}}
d_wo_inv_wo_wh1 = {'sku1': {'store1': 0, 'store2': 0}, 'sku2': {'store1': 0, 'store2': 0}}
current_stock1 = {'store1': {'sku1': 0, 'sku2': 5}, 'store2': {'sku1': 2, 'sku2': 0}}
Ex_total_days_wo_inv1 = {'sku1': {'store1': {'len': 2, 'sum': 0}, 'store2': {'len': 1, 'sum': 0}},
                          'sku2': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}}
expected_d_wo_inv1 = {'sku1': {'store1': 1, 'store2': 1}, 'sku2': {'store1': 0, 'store2': 1}}
expected_d_wo_inv_wo_wh1 = {'sku1': {'store1': 1, 'store2': 0}, 'sku2': {'store1': 0, 'store2': 1}}
expected_Ex_total_days_wo_inv1 = {'sku1': {'store1': {'len': 3, 'sum': 0.3333333333333333},
                                            'store2': {'len': 2, 'sum': 0}},
                                   'sku2': {'store1': {'len': 1, 'sum': 0}, 'store2': {'len': 1, 'sum': 1.0}}}

@pytest.mark.parametrize(
    "d_wo_inv, d_wo_inv_wo_wh, current_stock, Ex_total_days_wo_inv, expected_d_wo_inv, expected_d_wo_inv_wo_wh, expected_Ex_total_days_wo_inv",
    [(d_wo_inv1, d_wo_inv_wo_wh1, current_stock1, Ex_total_days_wo_inv1, expected_d_wo_inv1, expected_d_wo_inv_wo_wh1, expected_Ex_total_days_wo_inv1)]
)
def test_update_kpi_wo_inv(d_wo_inv, d_wo_inv_wo_wh, current_stock, Ex_total_days_wo_inv, expected_d_wo_inv, expected_d_wo_inv_wo_wh, expected_Ex_total_days_wo_inv):
    # Call the function with the input data
    updated_d_wo_inv, updated_d_wo_inv_wo_wh, updated_Ex_total_days_wo_inv = update_kpi_wo_inv(
        d_wo_inv, d_wo_inv_wo_wh, current_stock, Ex_total_days_wo_inv
    )

    # Perform assertions to check if the function behaves as expected
    assert updated_d_wo_inv == expected_d_wo_inv
    assert updated_d_wo_inv_wo_wh == expected_d_wo_inv_wo_wh
    assert updated_Ex_total_days_wo_inv == expected_Ex_total_days_wo_inv
