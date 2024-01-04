import pandas as pd


number_of_machine = 0
f_sales_v_fashion = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/f_sales_v_fashion.csv')
initial_stock_sku_store = pd.read_csv('/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv')
indexes_tuple_list = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10)]
list_intersection = [100652103000001, 100652103000002, 100652103000003, 100652103000004, 100652103000005, 100652103000006, 100652103000007, 100652103000008, 100652103000009, 100652103000010]


relevant_f_sales_v_fashion = f_sales_v_fashion[f_sales_v_fashion['sku'].isin(list_intersection[indexes_tuple_list[number_of_machine][0]:indexes_tuple_list[number_of_machine][1]])]
relevant_initial_stock_sku_store = initial_stock_sku_store[initial_stock_sku_store['sku'].isin(list_intersection[indexes_tuple_list[number_of_machine][0]:indexes_tuple_list[number_of_machine][1]])]


print("relevant_f_sales_v_fashion:", relevant_f_sales_v_fashion)
print("relevant_initial_stock_sku_store:", relevant_initial_stock_sku_store)
del f_sales_v_fashion
del initial_stock_sku_store