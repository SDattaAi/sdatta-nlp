import pandas as pd
import json
from clearml import Task

Task.add_requirements('requirements.txt')
task = Task.init(project_name="palmers_fashion", task_name="step2_fashion_strategy_calculation_task")
task.set_base_docker("palmerscr.azurecr.io/clean/nvidia-cuda_11.0.3-cudnn8-runtime-ubuntu20.04:1.0.1-private")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
#task.execute_remotely('ultra-high-cpu')
task.add_tags(['todelete'])

print("-----------------------------------Phase 0 - Update Arguments-----------------------------------")
args = {
    "number_of_this_machine": 0,
    'f_sales_v_fashion': pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/f_sales_v_fashion.csv'),
    'initial_stock_sku_store': pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv'),
    'list_intersection_skus': ['100511293000001', '100525187000003', '100535292000002', '100548702000003', '100542540000002', '100549814000001', '100548474000002', '100535248000001', '100539309000002', '100532494000004'],
    'indexes_tuple_list': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10)],
    'step1_load_all_relevant_data_for_fashion_task_id': '',
    'relevant_stores': ['51'],
}
print('Arguments: {}'.format(args))
number_of_this_machine = args["number_of_this_machine"]
f_sales_v_fashion = args["f_sales_v_fashion"]
initial_stock_sku_store = args["initial_stock_sku_store"]
list_intersection_skus = args["list_intersection_skus"]
indexes_tuple_list = args["indexes_tuple_list"]
step1_load_all_relevant_data_for_fashion_task_id = args["step1_load_all_relevant_data_for_fashion_task_id"]
relevant_stores = args["relevant_stores"]

if  step1_load_all_relevant_data_for_fashion_task_id != '':
    print("-----------------------------------need to be next task-----------------------------------")

    number_of_this_machine = 0
    relevant_f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].isin(list_intersection_skus[indexes_tuple_list[number_of_this_machine][0]:indexes_tuple_list[number_of_this_machine][1]])]
    relevant_initial_stock_sku_store = initial_stock_sku_store[initial_stock_sku_store['sku'].isin(list_intersection_skus[indexes_tuple_list[number_of_this_machine][0]:indexes_tuple_list[number_of_this_machine][1]])]


    # dict_sales : dict
    #     dict_sales[store][date] = [(sku, amount), ...]
    dict_sales = {}
    for store in relevant_f_sales_v_fashion['store'].unique():
        store_data = relevant_f_sales_v_fashion[relevant_f_sales_v_fashion['store'] == store]
        dict_sales[store] = {}
        for date in store_data['date'].astype(str).unique():
            date_data = store_data[store_data['date'] == date]
            dict_sales[store][date] = []
            for sku in date_data['sku'].unique():
                sku_data = date_data[date_data['sku'] == sku]
                amount = sku_data['sales'].sum()
                dict_sales[store][date].append((sku, amount))

    print("dict_sales:", dict_sales)


    # dict_stocks: dict
    #     dict_stocks[store][sku] = amount
    # if store == 'VZ01' take the value in 'VZ01' and do - sum of all other stores
    print(relevant_initial_stock_sku_store.columns)
    dict_stocks = {}
    for store in relevant_initial_stock_sku_store['store'].unique():
        if store == 'VZ01':
            dict_stocks[store] = {}
            for sku in relevant_initial_stock_sku_store[relevant_initial_stock_sku_store['store'] == store]['sku'].unique():
                sku_warehouse_data = relevant_initial_stock_sku_store[(relevant_initial_stock_sku_store['store'] == store) & (relevant_initial_stock_sku_store['sku'] == sku)]
                first_value_of_warehouse = sku_warehouse_data['initial_stock'].iloc[0]
                sku_warehouse_date = sku_warehouse_data['first_initial_stock_date'].iloc[0]
                other_stores_stock_after_warehouse = relevant_initial_stock_sku_store[(relevant_initial_stock_sku_store['sku'] == sku) & (relevant_initial_stock_sku_store['store'] != store) & (relevant_initial_stock_sku_store['first_initial_stock_date'] > sku_warehouse_date)]['initial_stock'].sum()
                dict_stocks[store][sku] = first_value_of_warehouse - other_stores_stock_after_warehouse
        else:
            dict_stocks[store] = {}
            for sku in relevant_initial_stock_sku_store[relevant_initial_stock_sku_store['store'] == store]['sku'].unique():
                dict_stocks[store][sku] = relevant_initial_stock_sku_store[(relevant_initial_stock_sku_store['store'] == store) & (relevant_initial_stock_sku_store['sku'] == sku)]['initial_stock'].iloc[0]

    print('dict_stocks', dict_stocks)

    start_dates = {}
    for store in relevant_initial_stock_sku_store['store'].unique():
        store_data = relevant_initial_stock_sku_store[relevant_initial_stock_sku_store['store'] == store]
        for sku in store_data['sku'].unique():
            sku_data = store_data[store_data['sku'] == sku]
            sku_data = sku_data[sku_data['initial_stock'] != 0]
            if not sku_data.empty:
                first_date = sku_data['first_initial_stock_date'].iloc[0]
                if first_date not in start_dates:
                    start_dates[first_date] = []
                start_dates[first_date].append((sku, store))

    print("start_dates:", start_dates)
    # end_dates: dict
    #     end_dates[date] = [(sku),...]
    # by the last sales that not 0 in the f_sales_v_fashion
    end_dates = {}

    for sku in f_sales_v_fashion['sku'].unique():
        sku_data = f_sales_v_fashion[f_sales_v_fashion['sku'] == sku]
        sku_data = sku_data[sku_data['sales'] != 0]
        if not sku_data.empty:
            last_date = sku_data['date'].max().strftime('%Y-%m-%d')
            if last_date not in end_dates:
                end_dates[last_date] = []
            end_dates[last_date].append(sku)

    print("end_dates:", end_dates)

    dict_arrivals_store_deliveries_path = r"date_to_store_deliveries_dict.json"
    dict_deliveries_from_warehouse_dict_path = r"deliveries_from_wharehouse_dict.json"
    with open(dict_arrivals_store_deliveries_path) as json_file:
        dict_arrivals_store_deliveries = json.load(json_file)
    with open(dict_deliveries_from_warehouse_dict_path) as json_file:
        dict_deliveries_from_warehouse = json.load(json_file)
    #%%
    fix_dict_arrivals_stors ={84:173,
     95:47,
     91:225,
     90:180,
     73:181,
     74:181,
     99:106,
     79:160,
     81:186,
     85:104,
     88:104,
     8:162,
     96:43,
     76:10,
     89:57,82:106,7:173,69:26}
    #%%
    for date,stores in dict_arrivals_store_deliveries.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    #%%
    for date,stores in dict_deliveries_from_warehouse.items():
        for store_problem,store_same in fix_dict_arrivals_stors.items():
            if store_same in stores:
                stores.append(store_problem)
    #%%
    unique_stores_in_2020 = set()
    for date,stores in dict_arrivals_store_deliveries.items():
        extract_year = pd.to_datetime(date).year
        if extract_year == 2020:
            # show all the unique stores that arrive stock in 2020
            unique_stores_in_2020.update(stores)


    strategy_names = "naive_bayes"
    stores_simulation = relevant_stores
    skus_simulation = list_intersection_skus



    #
    # [dict_deliveries_from_warehouse, dict_arrivals_store_deliveries, stores_simulation, skus_simulation,
    #  dict_sales, dict_stocks, start_date, end_date, start_dates, end_dates, strategy_names]
    print("-----------------------------------Phase 3 - calculate strategies-----------------------------------")




    print("-----------------------------------Phase 4 - upload reports-----------------------------------")

