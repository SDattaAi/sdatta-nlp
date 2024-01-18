import numpy as np
def update_info_for_kpi(accumulated_stocks: dict, current_stock: dict, Ex_i_s_r: dict, avg_integral_diff: dict,
                        margin_ratio: int = 3) -> tuple[dict, dict]:
    """
    This function update kpi dicts : Ex_i_s_r, avg_integral_diff
    Args:
    --------
    accumulated_stocks: dict
        accumulated_stocks[store][sku] = amount
    current_stock: dict
        current_stock[store][sku] = amount

    -------
    return: Ex_i_s_r, avg_integral_diff
    """
    for store in current_stock:
        total_stock, total_sales = 0, 0
        if store != "VZ01":
            for sku in current_stock[store]:
                total_stock += accumulated_stocks[store][sku]
                total_sales += accumulated_stocks[store][sku] - current_stock[store][sku]
                if total_stock == 0:
                    Ex_i_s_r[sku][store]['len'] += 1
                    Ex_i_s_r[sku][store]['sum'] += 0
                else:
                    Ex_i_s_r[sku][store]['len'] += 1
                    Ex_i_s_r[sku][store]['sum'] += total_sales / total_stock
                avg_integral_diff[sku][store]['len'] += 1
                avg_integral_diff[sku][store]['sum'] += current_stock[store][sku] - 1 if current_stock[store][sku] > 0 \
                    else margin_ratio
        for sku in current_stock['VZ01']:
            relevant_store_per_sku = [store for store in current_stock if sku in current_stock[store]]
            total_stock = np.sum([accumulated_stocks[store][sku] for store in relevant_store_per_sku])
            total_sales = total_stock - current_stock['VZ01'][sku]
            if total_stock == 0:
                print(f"total initialized stock in all stores for sku {sku} is 0")
            else:
                Ex_i_s_r[sku]['VZ01']['len'] += 1
                Ex_i_s_r[sku]['VZ01']['sum'] += total_sales / total_stock
    return Ex_i_s_r, avg_integral_diff