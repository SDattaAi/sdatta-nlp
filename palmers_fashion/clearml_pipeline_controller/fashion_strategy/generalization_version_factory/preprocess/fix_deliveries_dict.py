def fix_deliveries_dict(fix_dict_arrivals_stors:dict, dict_arrivals_store_deliveries:dict,dict_deliveries_from_wharehouse_dict:dict):
    for date,stores in dict_arrivals_store_deliveries.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    for date,stores in dict_deliveries_from_wharehouse_dict.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    return dict_arrivals_store_deliveries,dict_deliveries_from_wharehouse_dict