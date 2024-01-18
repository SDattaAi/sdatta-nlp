import numpy as np
def kill_and_save_results(accumulated_stocks: dict, d_wo_inv: dict, d_wo_inv_wo_wh: dict, Ex_i_s_r: dict,
                          avg_integral_diff: dict, Ex_total_days_wo_inv: dict, lose: dict, date: str, end_dates: dict,
                          MissedSales: dict, lamda: float = 0.1):
    """
    This function processes and calculates KPIs, and returns updated dictionaries along with final_kpi_res.

    Args:
    --------
    accumulated_stocks: dict
        Dictionary of accumulated stocks.
    d_wo_inv: dict
        Dictionary of days without inventory.
    d_wo_inv_wo_wh: dict
        Dictionary of days without inventory without warehouse.
    Ex_i_s_r: dict
        Dictionary of expected value of inventory sales ratio.
    avg_integral_diff: dict
        Dictionary of average integral differences.
    Ex_total_days_wo_inv: dict
        Dictionary of expected value of total days without inventory.
    lose: dict
        Dictionary of lose percentages.
    date: str
        Date of the simulation.
    end_dates: dict
        Dictionary of end dates.
    MissedSales: dict
        Dictionary of missed sales.
    lamda: float, optional
        Lambda value (default is 0.1).

    Returns:
    -------
    Tuple containing accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff,
    Ex_total_days_wo_inv, lose, MissedSales, final_kpi_res.
    """
    if date not in end_dates:
        return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, lose, MissedSales, {}
    final_kpi_res = {}
    for sku in end_dates[date]:
        for store in accumulated_stocks:
            if sku in accumulated_stocks[store]:
                lose_value_per_sku = d_wo_inv[sku]["VZ01"] * (np.exp(lamda * lose[sku]) - 1), lose[sku] if store == "VZ01" else None
                avg_integral_diff_sum_divde_avg_integral_diff = avg_integral_diff[sku][store]["sum"] / \
                                                                avg_integral_diff[sku][store]["len"] if \
                avg_integral_diff[sku][store]["len"] != 0 else None
                Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv = Ex_total_days_wo_inv[sku][store]["sum"] / \
                                                                      Ex_total_days_wo_inv[sku][store]["len"] if \
                Ex_total_days_wo_inv[sku][store]["len"] != 0 else None
                Ex_i_s_r_sum_divde_Ex_i_s_r = Ex_i_s_r[sku][store]["sum"] / Ex_i_s_r[sku][store]["len"] if \
                Ex_i_s_r[sku][store]["len"] != 0 else None
                final_kpi_res[f'{sku}_{store}'] = {f'days without stock': d_wo_inv[sku][store],
                                                   f'days without stock, without warehouse': d_wo_inv_wo_wh[sku][store],
                                                   f'expected value inventory sales ratio': Ex_i_s_r_sum_divde_Ex_i_s_r,
                                                   f'average integral difference': avg_integral_diff_sum_divde_avg_integral_diff,
                                                   f'expected value total days without inventory': Ex_total_days_wo_inv_sum_divde_Ex_total_days_wo_inv,
                                                   f'lose ratio': lose_value_per_sku,
                                                   f'missed sales': MissedSales[store][sku],
                                                   f'accumulated stock': accumulated_stocks[store][sku]}
            if sku in accumulated_stocks[store]:
                del accumulated_stocks[store][sku]
                del MissedSales[store][sku]
        del lose[sku], Ex_total_days_wo_inv[sku], Ex_i_s_r[sku], d_wo_inv_wo_wh[sku], d_wo_inv[sku], avg_integral_diff[
            sku]
    return accumulated_stocks, d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, lose, MissedSales, final_kpi_res
