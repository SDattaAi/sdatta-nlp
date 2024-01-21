import pytest
from fashion_strategy.simulation.generalization_version_factory.utils import kill_and_save_results

# Example inputs for the test case
accumulated_stocks1 = {
    "store1": {"sku1": 10, "sku2": 20},
    "store2": {"sku1": 15, "sku2": 25}
}

d_wo_inv1 = {
    "sku1": {"store1": 2, "store2": 3, 'VZ01': 100},
    "sku2": {"store1": 4, "store2": 1, 'VZ01': 100}
}

d_wo_inv_wo_wh1 = {
    "sku1": {"store1": 2, "store2": 3},
    "sku2": {"store1": 4, "store2": 1}
}

Ex_i_s_r1 = {
    "sku1": {"store1": {"sum": 50, "len": 5}, "store2": {"sum": 40, "len": 4}},
    "sku2": {"store1": {"sum": 30, "len": 3}, "store2": {"sum": 20, "len": 2}}
}

avg_integral_diff1 = {
    "sku1": {"store1": {"sum": 15, "len": 3}, "store2": {"sum": 10, "len": 3}},
    "sku2": {"store1": {"sum": 8, "len": 2}, "store2": {"sum": 5, "len": 1}}
}

Ex_total_days_wo_inv1 = {
    "sku1": {"store1": {"sum": 12, "len": 2}, "store2": {"sum": 8, "len": 1}},
    "sku2": {"store1": {"sum": 6, "len": 1}, "store2": {"sum": 4, "len": 1}}
}

lose1 = {
    "sku1": 0.5,
    "sku2": 0.12
}

date1 = "2024-01-01"

end_dates1 = {
    "2024-01-01": {"sku1": ["store1", "store2"]}
}

MissedSales1 = {
    "store1": {"sku1": 5, "sku2": 8},
    "store2": {"sku1": 3, "sku2": 6}
}

lamda1 = 0.1

# accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, lose, MissedSales, final_kpi_res
accumulated_stocks_output_expected1 = {'store1': {'sku2': 20}, 'store2': {'sku2': 25}}
d_wo_inv_output_expected1 = {'sku2': {'VZ01': 100, 'store1': 4, 'store2': 1}}
d_wo_inv_wo_wh_output_expected1 = {'sku2': {'store1': 4, 'store2': 1}}
Ex_i_s_r_output_expected1 = {'sku2': {'store1': {'len': 3, 'sum': 30}, 'store2': {'len': 2, 'sum': 20}}}
avg_integral_diff_output_expected1 = {'sku2': {'store1': {'len': 2, 'sum': 8}, 'store2': {'len': 1, 'sum': 5}}}
Ex_total_days_wo_inv_output_expected1 = {'sku2': {'store1': {'len': 1, 'sum': 6}, 'store2': {'len': 1, 'sum': 4}}}
lose_output_expected1 = {'sku2': 0.12}
MissedSales_output_expected1 = {'store1': {'sku2': 8}, 'store2': {'sku2': 6}}
final_kpi_res_output_expected1 = {'sku1_store1': {'accumulated stock': 10,
                 'average integral difference': 5.0,
                 'days without stock': 2,
                 'days without stock, without warehouse': 2,
                 'expected value inventory sales ratio': 10.0,
                 'expected value total days without inventory': 6.0,
                 'lose ratio': (5.127109637602412, None),
                 'missed sales': 5},
 'sku1_store2': {'accumulated stock': 15,
                 'average integral difference': 3.3333333333333335,
                 'days without stock': 3,
                 'days without stock, without warehouse': 3,
                 'expected value inventory sales ratio': 10.0,
                 'expected value total days without inventory': 8.0,
                 'lose ratio': (5.127109637602412, None),
                 'missed sales': 3}}
# Assuming the function is defined in a module named 'your_module'

@pytest.mark.parametrize(
    "accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, "
    "Ex_total_days_wo_inv, lose, date, end_dates, MissedSales, lamda, accumulated_stocks_output_expected,"
    "d_wo_inv_output_expected, d_wo_inv_wo_wh_output_expected, Ex_i_s_r_output_expected,"
    "avg_integral_diff_output_expected, Ex_total_days_wo_inv_output_expected, lose_output_expected,"
    "MissedSales_output_expected, final_kpi_res_output_expected",
    [(accumulated_stocks1, d_wo_inv1, d_wo_inv_wo_wh1, Ex_i_s_r1, avg_integral_diff1,
      Ex_total_days_wo_inv1, lose1, date1, end_dates1, MissedSales1, lamda1, accumulated_stocks_output_expected1,
      d_wo_inv_output_expected1, d_wo_inv_wo_wh_output_expected1, Ex_i_s_r_output_expected1,
        avg_integral_diff_output_expected1, Ex_total_days_wo_inv_output_expected1, lose_output_expected1,
        MissedSales_output_expected1, final_kpi_res_output_expected1)]
)
def test_kill_and_save_results(
    accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff,
    Ex_total_days_wo_inv, lose, date, end_dates, MissedSales, lamda, accumulated_stocks_output_expected,
    d_wo_inv_output_expected, d_wo_inv_wo_wh_output_expected, Ex_i_s_r_output_expected,
    avg_integral_diff_output_expected, Ex_total_days_wo_inv_output_expected, lose_output_expected,
MissedSales_output_expected, final_kpi_res_output_expected

):
    accumulated_stocks_result, d_wo_inv_result, d_wo_inv_wo_wh_result, Ex_i_s_r_result, avg_integral_diff_result, Ex_total_days_wo_inv_result, lose_result, MissedSales_result, final_kpi_res_result = kill_and_save_results(
        accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff,
        Ex_total_days_wo_inv, lose, date, end_dates, MissedSales, lamda
    )
    assert accumulated_stocks_result == accumulated_stocks_output_expected
    assert d_wo_inv_result == d_wo_inv_output_expected
    assert d_wo_inv_wo_wh_result == d_wo_inv_wo_wh_output_expected
    assert Ex_i_s_r_result == Ex_i_s_r_output_expected
    assert avg_integral_diff_result == avg_integral_diff_output_expected
    assert Ex_total_days_wo_inv_result == Ex_total_days_wo_inv_output_expected
    assert lose_result == lose_output_expected
    assert MissedSales_result == MissedSales_output_expected
    assert final_kpi_res_result == final_kpi_res_output_expected
