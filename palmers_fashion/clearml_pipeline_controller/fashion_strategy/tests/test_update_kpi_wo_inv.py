import pytest
from ... fashion_strategy.generalization_version_factory.utils_ import update_kpi_wo_inv

# Sample input and expected output dictionaries for testing
d_wo_inv1 = {'sku1': {'store1': 2, 'store2': 3, 'VZ01':100}, 'sku2': {'store1': 4, 'store2': 5, 'VZ01':100}}
d_wo_inv_wo_wh1 = {'sku1': {'store1': 2, 'store2': 3}, 'sku2': {'store1': 4, 'store2': 5}}
current_stock1 = {'store1': {'sku1': 0, 'sku2': 2}, 'store2': {'sku1': 2, 'sku2': 0}}
Ex_total_days_wo_inv1 = {'sku1': {'store1': {'len': 100, 'sum': 2}, 'store2': {'len': 100, 'sum': 3}},
                          'sku2': {'store1': {'len': 100, 'sum': 4}, 'store2': {'len': 100, 'sum': 5}}}


expected_d_wo_inv1 = {'sku1': {'store1': 3, 'store2': 3, 'VZ01': 100}, 'sku2': {'store1': 4, 'store2': 6, 'VZ01': 100}}
expected_d_wo_inv_wo_wh1 = {'sku1': {'store1': 3, 'store2': 3}, 'sku2': {'store1': 4, 'store2': 6}}
expected_Ex_total_days_wo_inv1 = {'sku1': {'store1': {'len': 101, 'sum': 3}, 'store2': {'len': 101, 'sum': 3}},
                                'sku2': {'store1': {'len': 101, 'sum': 4}, 'store2': {'len': 101, 'sum': 6}}}

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
