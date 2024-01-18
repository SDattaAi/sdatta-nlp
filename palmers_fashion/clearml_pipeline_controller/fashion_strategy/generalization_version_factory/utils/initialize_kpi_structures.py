def initialize_kpi_structures(dict_stocks: dict, skus_simulation: list) -> (dict, dict, dict, dict, dict, dict):
    """
    This function initialize all the kpi dicts : d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv
    Args:
    --------
    stores_simulation : list
        list of stores to simulate
    skus_simulation : list
        list of skus to simulate

    -------
    return:  d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv
    """
    d_wo_inv = {}
    d_wo_inv_wo_wh = {}
    Ex_i_s_r = {}
    avg_integral_diff = {}
    Ex_total_days_wo_inv = {}
    loose = {}
    for sku in skus_simulation:
        d_wo_inv[sku] = {}
        d_wo_inv_wo_wh[sku] = {}
        Ex_i_s_r[sku] = {}
        avg_integral_diff[sku] = {}
        Ex_total_days_wo_inv[sku] = {}
        loose[sku] = 0
        for store in dict_stocks:
            d_wo_inv[sku][store] = 0
            d_wo_inv_wo_wh[sku][store] = 0
            Ex_i_s_r[sku][store] = {'len': 0, 'sum': 0}
            avg_integral_diff[sku][store] = {'len': 0, 'sum': 0}
            Ex_total_days_wo_inv[sku][store] = {'len': 0, 'sum': 0}

    return d_wo_inv, d_wo_inv_wo_wh, Ex_i_s_r, avg_integral_diff, Ex_total_days_wo_inv, loose