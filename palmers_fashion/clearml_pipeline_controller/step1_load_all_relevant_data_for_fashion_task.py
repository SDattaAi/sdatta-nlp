
import pandas as pd
from sdatta_learn.remote_running.parallelization import split_ids_index_per_machine
from sdatta_learn.loader.load_from_postgres import get_sales_between_dates_and_stores, get_fashion_skus_from_artikelstamm
from clearml import Task, Dataset

import warnings
warnings.filterwarnings("ignore")
Task.add_requirements('requirements.txt')
task = Task.init(project_name="palmers/training", task_name="step1_load_all_relevant_data_for_fashion_task")
task.set_base_docker("palmerscr.azurecr.io/clean/nvidia-cuda_11.0.3-cudnn8-runtime-ubuntu20.04:1.0.1-private")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['todelete'])


print("-----------------------------------Phase 0 - Update Arguments-----------------------------------")
args = {
    "number_of_machines": 10,
    'relevant_stores': ['51'],
    "pg_port": "5432",
    "pg_user": "datatiger",
    "pg_password": "Hwhiupwj6SZ4Sq",
    "pg_host": "sdatta-pg.postgres.database.azure.com",
    "pg_database": "postgres",
    "f_sales_v_table_name": "f_sales_v",
    "artikelstamm_table_name": "l_artikelstamm",
    "start_date_f_sales_v": "2020-01-01",
    "end_date_f_sales_v": "2020-03-01"
}
print('Arguments: {}'.format(args))
number_of_machines = args["number_of_machines"]
relevant_stores = args["relevant_stores"]
pg_port = args["pg_port"]
pg_user = args["pg_user"]
pg_password = args["pg_password"]
pg_host = args["pg_host"]
pg_database = args["pg_database"]
f_sales_v_table_name = args["f_sales_v_table_name"]
artikelstamm_table_name = args["artikelstamm_table_name"]
formatted_relevant_stores = ", ".join(f"'{store}'" for store in relevant_stores)
start_date_f_sales_v = args["start_date_f_sales_v"]
end_date_f_sales_v = args["end_date_f_sales_v"]
print("-----------------------------------Phase 1 - Load f_sales_v_fashion and initial_stock_sku_store-----------------------------------")
f_sales_v = get_sales_between_dates_and_stores(pg_host=pg_host,
                                               pg_port=pg_port,
                                               pg_user=pg_user,
                                               pg_password=pg_password,
                                               pg_database=pg_database,
                                               start_date=start_date_f_sales_v,
                                               end_date=end_date_f_sales_v,
                                               formatted_stores=formatted_relevant_stores,)
f_sales_v = f_sales_v.rename(columns={'outlet':'store',
                                      'mat_no':'sku',
                                      'quantity':'sales',
                                      })[['store', 'sku', 'date', 'sales']]
f_sales_v['date'] = pd.to_datetime(f_sales_v['date'])
f_sales_v['sales'] = f_sales_v['sales'].astype(int)
f_sales_v['sku'] = f_sales_v['sku'].astype(str)
f_sales_v['store'] = f_sales_v['store'].astype(str)

print("f_sales_v:", f_sales_v)
print("list(f_sales_v.columns):", list(f_sales_v.columns))

fashion_skus = get_fashion_skus_from_artikelstamm(pg_host=pg_host,
                                                    pg_port=pg_port,
                                                    pg_user=pg_user,
                                                    pg_password=pg_password,
                                                    pg_database=pg_database,
                                                    artikelstamm_table_name=artikelstamm_table_name)

fashion_skus = fashion_skus.rename(columns={'article':'sku'})
fashion_skus['sku'] = fashion_skus['sku'].astype(str)
print("fashion_skus:", fashion_skus)
f_sales_v_fashion = f_sales_v[f_sales_v['sku'].astype(str).isin(fashion_skus['sku'])]
print("f_sales_v_fashion:", f_sales_v_fashion)
f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].isin(fashion_skus['sku'])]
# initial_stock_sku_store from dataset clearml
initial_stocks_path = Dataset.get(dataset_project="palmers_fashion", dataset_name="initial_stocks").get_local_copy()
print('initial_stocks_path:',initial_stocks_path)
initial_stock_sku_store = pd.read_csv(initial_stocks_path + '/initial_stock_sku_store.csv')
#initial_stock_sku_store = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv')
initial_stock_sku_store['sku'] = initial_stock_sku_store['sku'].astype(str)
print("initial_stock_sku_store:", initial_stock_sku_store)
print("-----------------------------------Phase 2 - Filter relevant skus-----------------------------------")
list1 = set(f_sales_v_fashion[(f_sales_v_fashion['date'] > '2019-01-01') & (f_sales_v_fashion['sales'] > 0)]['sku'].unique())
print("list1:", list1)
list2 = set(initial_stock_sku_store[initial_stock_sku_store['store'] == 'VZ01']['sku'].unique())
print("list2:", list2)
list_intersection = list1.intersection(list2)
print("list_intersection:", list_intersection)
indexes_tuple_list = split_ids_index_per_machine(len(list_intersection), number_of_machines)
print("list_intersection:", list_intersection)
print("indexes_tuple_list:", indexes_tuple_list)

print("-----------------------------------Phase 1 - Upload artifacts-----------------------------------")
task.upload_artifact("f_sales_v_fashion", f_sales_v_fashion, wait_on_upload=True)
task.upload_artifact("initial_stock_sku_store", initial_stock_sku_store, wait_on_upload=True)
task.upload_artifact("list_intersection", list_intersection, wait_on_upload=True)
task.upload_artifact("indexes_tuple_list", indexes_tuple_list, wait_on_upload=True)
