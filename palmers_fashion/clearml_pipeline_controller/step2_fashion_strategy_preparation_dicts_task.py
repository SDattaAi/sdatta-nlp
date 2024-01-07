import pandas as pd
import json
from clearml import Task
import pickle

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
    'step1_load_all_relevant_data_for_fashion_task_id': '8d1a774f627f4f718c4b63370f54f0ee',
    'relevant_stores': ['51', 'VZ01'],
    "start_date": "2020-01-01",
    "end_date": "2020-02-28"
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
    print("relevant_skus_to_this_machine:", relevant_skus_to_this_machine)

    print("-----------------------------------Phase 1 - take artifacts from task1-----------------------------------")
    print("f_sales_v_fashion.info():", f_sales_v_fashion.info())
    print("initial_stock_sku_store.info():", initial_stock_sku_store.info())
    f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].astype(str).isin(relevant_skus_to_this_machine)]
    initial_stock_sku_store = initial_stock_sku_store[initial_stock_sku_store['sku'].astype(str).isin(relevant_skus_to_this_machine)]
    print("f_sales_v_fashion2:", f_sales_v_fashion)
    print("initial_stock_sku_store2:", initial_stock_sku_store)
    f_sales_v_fashion['date'] = pd.to_datetime(f_sales_v_fashion['date'])

    print("-----------------------------------Phase 2 - create dicts for calculations-----------------------------------")
    # dict_sales : dict
    #     dict_sales[store][date] = [(sku, amount), ...]
    dict_sales = {}
    for store in f_sales_v_fashion['store'].unique():
        store_data = f_sales_v_fashion[f_sales_v_fashion['store'] == store]
        dict_sales[store] = {}
        for date in store_data['date'].astype(str).unique():
            date_data = store_data[store_data['date'] == date]
            dict_sales[store][date] = []
            for sku in date_data['sku'].unique():
                sku_data = date_data[date_data['sku'] == sku]
                amount = sku_data['sales'].sum()
                dict_sales[store][date].append((sku, amount))



    # dict_stocks: dict
    #     dict_stocks[store][sku] = amount
    # if store == 'VZ01' take the value in 'VZ01' and do - sum of all other stores
    print(initial_stock_sku_store.columns)
    dict_stocks = {}
    for store in relevant_stores:
        if store == 'VZ01':
            dict_stocks[store] = {}
            for sku in initial_stock_sku_store[initial_stock_sku_store['store'] == store]['sku'].unique():
                sku_warehouse_data = initial_stock_sku_store[(initial_stock_sku_store['store'] == store) & (initial_stock_sku_store['sku'] == sku)]
                first_value_of_warehouse = sku_warehouse_data['initial_stock'].iloc[0]
                sku_warehouse_date = sku_warehouse_data['first_initial_stock_date'].iloc[0]
                other_stores_stock_after_warehouse = initial_stock_sku_store[(initial_stock_sku_store['sku'] == sku) & (initial_stock_sku_store['store'] != store) & (initial_stock_sku_store['first_initial_stock_date'] > sku_warehouse_date)]['initial_stock'].sum()
                dict_stocks[store][sku] = first_value_of_warehouse - other_stores_stock_after_warehouse
        else:
            dict_stocks[store] = {}
            for sku in initial_stock_sku_store[initial_stock_sku_store['store'] == store]['sku'].unique():
                dict_stocks[store][sku] = initial_stock_sku_store[(initial_stock_sku_store['store'] == store) & (initial_stock_sku_store['sku'] == sku)]['initial_stock'].iloc[0]


    start_dates = {}
    for store in relevant_stores:
        store_data = initial_stock_sku_store[initial_stock_sku_store['store'] == store]
        for sku in store_data['sku'].unique():
            sku_data = store_data[store_data['sku'] == sku]
            sku_data = sku_data[sku_data['initial_stock'] != 0]
            if not sku_data.empty:
                first_date = sku_data['first_initial_stock_date'].iloc[0]
                if first_date not in start_dates:
                    start_dates[first_date] = []
                start_dates[first_date].append((sku, store))

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


    print("dict_arrivals_store_deliveries:", dict_arrivals_store_deliveries)
    print("dict_deliveries_from_warehouse:", dict_deliveries_from_warehouse)
    print("stores_simulation:", stores_simulation)
    print("skus_simulation:", skus_simulation)
    print("dict_sales:", dict_sales)
    print("dict_stocks:", dict_stocks)
    print("start_dates:", start_dates)
    print("end_dates:", end_dates)
    print("strategy_names:", strategy_names)


    print("-----------------------------------Phase 4 - upload dicts & array artifacts-----------------------------------")
    task.upload_artifact('dict_deliveries_from_warehouse', artifact_object=dict_deliveries_from_warehouse)
    task.upload_artifact('dict_arrivals_store_deliveries', artifact_object=dict_arrivals_store_deliveries)
    task.upload_artifact('stores_simulation', artifact_object=stores_simulation)
    task.upload_artifact('skus_simulation', artifact_object=skus_simulation)
    task.upload_artifact('dict_sales', artifact_object=dict_sales)
    task.upload_artifact('dict_stocks', artifact_object=dict_stocks)
    task.upload_artifact('start_dates', artifact_object=start_dates)
    task.upload_artifact('end_dates', artifact_object=end_dates)
    task.upload_artifact('strategy_names', artifact_object=strategy_names)

