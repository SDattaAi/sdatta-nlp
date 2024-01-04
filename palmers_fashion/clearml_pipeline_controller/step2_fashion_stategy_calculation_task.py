import pandas as pd

print("-----------------------------------Phase 0 - Update Arguments-----------------------------------")
args = {
    "number_of_this_machine": 0,
    'f_sales_v_fashion': pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/f_sales_v_fashion.csv'),
    'initial_stock_sku_store': pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv'),
    'list_intersection': [100652103000001, 100652103000002, 100652103000003, 100652103000004, 100652103000005, 100652103000006, 100652103000007, 100652103000008, 100652103000009, 100652103000010],
    'indexes_tuple_list': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10)]
}
print('Arguments: {}'.format(args))
number_of_this_machine = args["number_of_this_machine"]
f_sales_v_fashion = args["f_sales_v_fashion"]
initial_stock_sku_store = args["initial_stock_sku_store"]
list_intersection = args["list_intersection"]
indexes_tuple_list = args["indexes_tuple_list"]
print("-----------------------------------Phase 1 - Load f_sales_v_fashion & initial_stock_sku_store & list_intersection & indexes_tuple_list-----------------------------------")

print('-----------------------------------Phase 2 - Filter relevant skus-----------------------------------')

relevant_f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].isin(list_intersection[indexes_tuple_list[number_of_this_machine][0]:indexes_tuple_list[number_of_this_machine][1]])]
relevant_initial_stock_sku_store = initial_stock_sku_store[initial_stock_sku_store['sku'].isin(list_intersection[indexes_tuple_list[number_of_this_machine][0]:indexes_tuple_list[number_of_this_machine][1]])]


print("relevant_f_sales_v_fashion:", relevant_f_sales_v_fashion)
print("relevant_initial_stock_sku_store:", relevant_initial_stock_sku_store)
del f_sales_v_fashion
del initial_stock_sku_store
print("-----------------------------------Phase 3 - calculate strategies-----------------------------------")




print("-----------------------------------Phase 4 - upload reports-----------------------------------")

