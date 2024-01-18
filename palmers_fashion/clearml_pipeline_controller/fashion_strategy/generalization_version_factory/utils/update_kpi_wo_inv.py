def update_kpi_wo_inv(d_wo_inv: dict, d_wo_inv_wo_wh: dict, current_stock: dict, Ex_total_days_wo_inv: dict) -> tuple[
    dict, dict, dict]:
    """
    This function update kpi dicts : d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    Args:
    --------
    d_wo_inv: dict
        d_wo_inv[sku][store] = amount
    d_wo_inv_wo_wh: dict
        d_wo_inv_wo_wh[sku]['VZ01'] = amount
    current_stock: dict
        current_stock[store][sku] = amount

    -------
    return: d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv
    """
    for store in current_stock:
        for sku in current_stock[store]:
            Ex_total_days_wo_inv[sku][store]['len'] += 1
            if current_stock[store][sku] == 0:
                d_wo_inv[sku][store] += 1
                Ex_total_days_wo_inv[sku][store]['sum'] += 1
                if store != "VZ01":
                    d_wo_inv_wo_wh[sku][store] += 1
    return d_wo_inv, d_wo_inv_wo_wh, Ex_total_days_wo_inv