
import pandas as pd
from sdatta_learn.remote_running.parallelization import split_ids_index_per_machine


print("-----------------------------------Phase 0 - Update Arguments-----------------------------------")
args = {
    "number_of_machines": 10
}
print('Arguments: {}'.format(args))
number_of_machines = args["number_of_machines"]

print("-----------------------------------Phase 1 - Load f_sales_v_fashion and initial_stock_sku_store-----------------------------------")
f_sales_v_fashion = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/f_sales_v_fashion.csv')
f_sales_v_fashion = f_sales_v_fashion.rename(columns={'total_sales':'sales'})
initial_stock_sku_store = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv')

print("-----------------------------------Phase 2 - Filter relevant skus-----------------------------------")
list1 = set(f_sales_v_fashion[(f_sales_v_fashion['date'] > '2019-01-01') & (f_sales_v_fashion['sales'] > 0)]['sku'].unique())
list2 = initial_stock_sku_store[initial_stock_sku_store['store'] == 'VZ01']['sku'].unique()
list_intersection = list1.intersection(list2)
indexes_tuple_list = split_ids_index_per_machine(len(list_intersection), number_of_machines)

print("indexes_tuple_list:", indexes_tuple_list)
print("list_intersection:", list_intersection)
print("-----------------------------------Phase 1 - Upload artifacts-----------------------------------")
# task.upload_artifact("f_sales_v_fashion", f_sales_v_fashion, wait_on_upload=True)
# task.upload_artifact("initial_stock_sku_store", initial_stock_sku_store, wait_on_upload=True)
# task.upload_artifact("list_intersection", list_intersection, wait_on_upload=True)
# task.upload_artifact("indexes_tuple_list", indexes_tuple_list, wait_on_upload=True)
