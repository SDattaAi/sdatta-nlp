from ... fashion_strategy.generalization_version_factory.utils_ import initialize_kpi_structures
import pytest

skus_simulation1 = ['sku1', 'sku2']
dict_stocks1 = {'store1': {'sku1': 50, 'sku2': 30}, 'store2': {'sku1': 60, 'sku2': 20}}
d_wo_inv1 =  {'sku1': {'store1': 0, 'store2': 0}, 'sku2': {'store1': 0, 'store2': 0}}
d_wo_inv_wo_wh1 =  {'sku1': {'store1': 0, 'store2': 0}, 'sku2': {'store1': 0, 'store2': 0}}
Ex_i_s_r1 =  {'sku1': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}, 'sku2': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}}
avg_integral_diff1 =  {'sku1': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}, 'sku2': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}}
Ex_total_days_wo_inv1 =  {'sku1': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}, 'sku2': {'store1': {'len': 0, 'sum': 0}, 'store2': {'len': 0, 'sum': 0}}}
loose1 =  {'sku1': 0, 'sku2': 0}
expected1 = (d_wo_inv1, d_wo_inv_wo_wh1, Ex_i_s_r1, avg_integral_diff1, Ex_total_days_wo_inv1, loose1)

@pytest.mark.parametrize("skus_simulation, dict_stocks, expected", [(skus_simulation1, dict_stocks1, expected1)])
def test_initialize_kpi_structures(dict_stocks, skus_simulation, expected):
    d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose = initialize_kpi_structures(dict_stocks, skus_simulation)
    assert expected == (d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose)
    assert expected[0].keys() == expected[1].keys() == expected[2].keys() == expected[3].keys() == expected[4].keys() == expected[5].keys()

