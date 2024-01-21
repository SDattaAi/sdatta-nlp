import json
import pickle
import pandas as pd
from clearml import Task
from sdatta_learn.fashion_strategy.simulation.input_dicts_validation import *
from fashion_strategy.simulation.generalization_version_factory.preprocess import *

Task.add_requirements('requirements.txt')
task = Task.init(project_name="palmers_fashion", task_name="step2_fashion_strategy_preparation_dicts_task")
task.set_base_docker("palmerscr.azurecr.io/clean/nvidia-cuda_11.0.3-cudnn8-runtime-ubuntu20.04:1.0.1-private")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['todelete'])

print("-----------------------------------Phase 0 - Update Arguments-----------------------------------")
args = {
    "number_of_this_machine": 0,
    'f_sales_v_fashion': pd.DataFrame(),
    'initial_stock_sku_store': pd.DataFrame(),
    'list_intersection_skus': ['100537293000001', '100539815000003'],
    'indexes_tuple_list': [(0, 1), (1, 2)],
    'step1_load_all_relevant_data_for_fashion_task_id': '98c4260e1d7644e28bb6c236c71db32b',
    'relevant_stores': ["76", "4134", "4904", "10", "100", "109", "11", "117", "133", "135", "141", "143", "164", "181", "183", "185", "201", "213", "214", "22", "3005", "3202", "4104", "4123", "4129", "42", "45", "46", "4803", "4906", "5", "67", "68", "7", "73", "8", "82", "88", "89", "104", "174", "3208", "37", "63", "91", "96", "202", "21", "90", "95", "121", "144", "147", "173", "4133", "47", "81", "170", "28", "172", "15", "166", "217", "27", "4", "51", "114", "122", "160", "3", "69", "182", "26", "105", "106", "119", "130", "136", "149", "150", "156", "159", "162", "167", "168", "171", "179", "18", "180", "184", "186", "189", "203", "215", "218", "220", "221", "225", "29", "44", "4805", "50", "52", "55", "56", "61", "64", "74", "79", "84", "85", "99", "152", "163", "175", "216", "219", "3245", "57", "3205", "43", "226", "35", "36", "123", "188", "VZ01"],
    'start_date' : '2018-01-01',
    'end_date' : '2023-12-01'
}

task.connect(args)
print('Arguments: {}'.format(args))
number_of_this_machine = args["number_of_this_machine"]
f_sales_v_fashion = args["f_sales_v_fashion"]
initial_stock_sku_store = args["initial_stock_sku_store"]
list_intersection_skus = args["list_intersection_skus"]
indexes_tuple_list = args["indexes_tuple_list"]
step1_load_all_relevant_data_for_fashion_task_id = args["step1_load_all_relevant_data_for_fashion_task_id"]
relevant_stores = args["relevant_stores"]
start_date = args["start_date"]
end_date = args["end_date"]

if  step1_load_all_relevant_data_for_fashion_task_id != '':
    step1_task = Task.get_task(task_id=step1_load_all_relevant_data_for_fashion_task_id)
    # dict
    f_sales_v_fashion_path = step1_task.artifacts['f_sales_v_fashion'].get_local_copy()
    f_sales_v_fashion = pd.read_csv(f_sales_v_fashion_path)
    print("f_sales_v_fashion loaded")
    initial_stock_sku_store_path = step1_task.artifacts['initial_stock_sku_store'].get_local_copy()
    initial_stock_sku_store = pd.read_csv(initial_stock_sku_store_path)
    print("initial_stock_sku_store loaded")
    list_intersection_skus_path = step1_task.artifacts['list_intersection_skus'].get_local_copy()
    with open(list_intersection_skus_path, 'rb') as pickle_file:
        list_intersection_skus = pickle.load(pickle_file)
    print("list_intersection_skus loaded")
    indexes_tuple_list_path = step1_task.artifacts['indexes_tuple_list'].get_local_copy()
    with open(indexes_tuple_list_path, 'rb') as pickle_file:
        indexes_tuple_list = pickle.load(pickle_file)
    print("indexes_tuple_list loaded")
    print("f_sales_v_fashion:", f_sales_v_fashion)
    print("initial_stock_sku_store:", initial_stock_sku_store)
    print("list_intersection_skus:", list_intersection_skus)
    print("indexes_tuple_list:", indexes_tuple_list)
    print("relevant_stores:", relevant_stores)
    print("number_of_this_machine:", number_of_this_machine)

    relevant_skus_to_this_machine = list_intersection_skus[indexes_tuple_list[number_of_this_machine][0]:indexes_tuple_list[number_of_this_machine][1]]
   # relevant_skus_to_this_machine = ['100060075000001']
    print("relevant_skus_to_this_machine:", relevant_skus_to_this_machine)

    print("-----------------------------------Phase 1 - take artifacts from task1-----------------------------------")
    print("f_sales_v_fashion['sku'].num_unique():", f_sales_v_fashion['sku'].nunique())
    print("initial_stock_sku_store['sku'].num_unique():", initial_stock_sku_store['sku'].nunique())
    f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].astype(str).isin(relevant_skus_to_this_machine)]
    initial_stock_sku_store = initial_stock_sku_store[initial_stock_sku_store['sku'].astype(str).isin(relevant_skus_to_this_machine)]
    print("f_sales_v_fashion2['sku'].num_unique():", f_sales_v_fashion['sku'].nunique())
    print("initial_stock_sku_store2['sku'].num_unique():", initial_stock_sku_store['sku'].nunique())
    f_sales_v_fashion['date'] = pd.to_datetime(f_sales_v_fashion['date'])

    print("-----------------------------------Phase 2 - create dicts for calculations-----------------------------------")
    # dict_sales : dict
    #     dict_sales[store][date] = [(sku, amount), ...]
    print("dict_sales")
    dict_sales = dict_sales_from_f_sales_v(f_sales_v_fashion)

    print("dict_stocks")
    dict_stocks = dict_stocks_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores)

    print("start_dates")
    start_dates = start_dates_from_initial_stock_sku_store(initial_stock_sku_store, relevant_stores)

    print("end_dates")
    end_dates = end_dates_from_f_sales_v(f_sales_v_fashion)

    dict_arrivals_store_deliveries_path = r"date_to_store_deliveries_dict.json"
    dict_deliveries_from_warehouse_dict_path = r"deliveries_from_wharehouse_dict.json"
    with open(dict_arrivals_store_deliveries_path) as json_file:
        dict_arrivals_store_deliveries = json.load(json_file)
    with open(dict_deliveries_from_warehouse_dict_path) as json_file:
        dict_deliveries_from_warehouse = json.load(json_file)
    #%%
    fix_dict_arrivals_stores ={84:173,
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
        for store_problem,store_same in fix_dict_arrivals_stores.items():
            if store_same in stores:
                stores.append(store_problem)
    #%%
    for date,stores in dict_deliveries_from_warehouse.items():
        for store_problem,store_same in fix_dict_arrivals_stores.items():
            if store_same in stores:
                stores.append(store_problem)
    #%%
    unique_stores_in_2020 = set()
    for date,stores in dict_arrivals_store_deliveries.items():
        extract_year = pd.to_datetime(date).year
        if extract_year == 2020:
            # show all the unique stores that arrive stock in 2020
            unique_stores_in_2020.update(stores)



    print(" fix start_dates")






    start_dates = create_fix_start_dates(start_dates, end_dates)

    print("delete negative stock from warehouse")

    _, list_sku_to_delete = validate_stock_not_negative_for_warehouse(dict_stocks)
    print("list_sku_to_delete: ", list_sku_to_delete)

    # remove from relevant_skus_to_this_machine list_sku_to_delete

    relevant_skus_to_this_machine = [sku for sku in relevant_skus_to_this_machine if sku not in list_sku_to_delete]
    dict_stocks = {store: {sku: stock for sku, stock in store_dict.items() if sku not in list_sku_to_delete} for store, store_dict in dict_stocks.items()}
    dict_sales = {store: {date: [(sku, amount) for sku, amount in date_list if sku not in list_sku_to_delete] for date, date_list in store_dict.items()} for store, store_dict in dict_sales.items()}
    start_dates = {date: [(sku, store) for sku, store in date_list if sku not in list_sku_to_delete] for date, date_list in start_dates.items()}
    end_dates = {date: [sku for sku in date_list if sku not in list_sku_to_delete] for date, date_list in end_dates.items()}


    strategy_names = "naive_bayes"
    stores_simulation = relevant_stores
    skus_simulation = relevant_skus_to_this_machine

    print("number of skus:", len(skus_simulation))

    validate_stock_not_negative_for_warehouse_result, _ = validate_stock_not_negative_for_warehouse(dict_stocks)
    validate_start_end_dates_result = validate_start_end_dates(start_dates, end_dates)
    validate_store_sku_identifiers_result = validate_store_sku_identifiers(dict_stocks, dict_sales)
    validate_sales_date_format_result = validate_sales_date_format(dict_sales)
    validate_sku_availability_result = validate_sku_availability(dict_stocks, dict_sales)
    validate_sales_dates_within_simulation_period_result = validate_sales_dates_within_simulation_period(dict_sales,
                                                                                                         start_date,
                                                                                                         end_date)
    validate_non_empty_inputs_result = validate_non_empty_inputs(dict_stocks, dict_sales)
    validate_warehouse_delivery_dates_and_stores_result = validate_warehouse_delivery_dates_and_stores(
        dict_deliveries_from_warehouse)
    validate_store_delivery_dates_and_stores_result = validate_store_delivery_dates_and_stores(
        dict_arrivals_store_deliveries)
    validate_non_empty_deliveries_result = validate_non_empty_deliveries(dict_deliveries_from_warehouse,
                                                                         dict_arrivals_store_deliveries)

    print("validate_stock_not_negative_for_warehouse_result: ", validate_stock_not_negative_for_warehouse_result)
    print("validate_start_end_dates_result: ", validate_start_end_dates_result)
    print("validate_store_sku_identifiers_result: ", validate_store_sku_identifiers_result)
    print("validate_sales_date_format_result: ", validate_sales_date_format_result)
    print("validate_sku_availability_result: ", validate_sku_availability_result)
    print("validate_sales_dates_within_simulation_period_result: ",
          validate_sales_dates_within_simulation_period_result)
    print("validate_non_empty_inputs_result: ", validate_non_empty_inputs_result)
    print("validate_warehouse_delivery_dates_and_stores_result: ", validate_warehouse_delivery_dates_and_stores_result)
    print("validate_store_delivery_dates_and_stores_result: ", validate_store_delivery_dates_and_stores_result)
    print("validate_non_empty_deliveries_result: ", validate_non_empty_deliveries_result)

    print("-----------------------------------Phase 4 - upload dicts & array artifacts-----------------------------------")
    # upload json
    task.upload_artifact('dict_deliveries_from_warehouse', artifact_object=dict_deliveries_from_warehouse)
    task.upload_artifact('dict_arrivals_store_deliveries', artifact_object=dict_arrivals_store_deliveries)
    task.upload_artifact('skus_simulation', artifact_object=skus_simulation)
    task.upload_artifact('dict_sales', artifact_object=dict_sales)
    task.upload_artifact('dict_stocks', artifact_object=dict_stocks)
    task.upload_artifact('start_dates', artifact_object=start_dates)
    task.upload_artifact('end_dates', artifact_object=end_dates)
    task.upload_artifact('strategy_names', artifact_object=strategy_names)

