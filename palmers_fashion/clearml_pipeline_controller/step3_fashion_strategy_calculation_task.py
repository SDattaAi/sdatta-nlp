import json
import pickle
from clearml import Task
from sdatta_learn.fashion_strategy.simulation.simulation_general import main_simulation, apply_strategy_opt_sw_avg, \
    apply_strategy_naive_bayes

from sdatta_learn.fashion_strategy.simulation.input_dicts_validation import *
Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step3_fashion_strategy_calculation_task")
task.set_base_docker("palmerscr.azurecr.io/clean/ubuntu22.04-private-pip:1.0.2")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['todelete'])

args = {
    "dict_arrivals_store_deliveries": {},
    "dict_deliveries_from_warehouse": {},
    "stores_simulation": [],
    "skus_simulation": [],
    "dict_sales": {},
    "dict_stocks": {},
    "start_dates": {},
    "end_dates": {},
    "strategy_names": "naive_bayes",
    "step2_fashion_strategy_calculation_task_id": "",
    "start_date": '2018-01-01',
    "end_date": '2023-12-01',
}
print("-----------------------------------Phase 1 - update args-----------------------------------")

task.connect(args)
print('Arguments: {}'.format(args))
start_date = args["start_date"]
end_date = args["end_date"]
dict_arrivals_store_deliveries = args["dict_arrivals_store_deliveries"]
dict_deliveries_from_warehouse = args["dict_deliveries_from_warehouse"]
stores_simulation = args["stores_simulation"]
skus_simulation = args["skus_simulation"]
dict_sales = args["dict_sales"]
dict_stocks = args["dict_stocks"]
start_dates = args["start_dates"]
end_dates = args["end_dates"]
strategy_names = args["strategy_names"]
step2_fashion_strategy_calculation_task_id = args["step2_fashion_strategy_calculation_task_id"]

print("-----------------------------------Phase 2 - load artifact-----------------------------------")
if step2_fashion_strategy_calculation_task_id != "":
    print("step2_fashion_strategy_calculation_task_id is not empty, start strategy")
    print("step2_fashion_strategy_calculation_task_id: ", step2_fashion_strategy_calculation_task_id)
    step2_task = Task.get_task(task_id=step2_fashion_strategy_calculation_task_id)
    step2_task_artifacts = step2_task.artifacts
    dict_deliveries_from_warehouse_path = step2_task_artifacts['dict_deliveries_from_warehouse'].get_local_copy()
    # json read
    with open(dict_deliveries_from_warehouse_path, 'r') as f:
        dict_deliveries_from_warehouse = json.load(f)
    dict_arrivals_store_deliveries_path = step2_task_artifacts['dict_arrivals_store_deliveries'].get_local_copy()
    with open(dict_arrivals_store_deliveries_path, 'r') as f:
        dict_arrivals_store_deliveries = json.load(f)
    skus_simulation_path = step2_task_artifacts['skus_simulation'].get_local_copy()
    with open(skus_simulation_path, 'rb') as f:
        skus_simulation = pickle.load(f)
    print("skus_simulation: ", skus_simulation)
    dict_sales_path = step2_task_artifacts['dict_sales'].get_local_copy()
    with open(dict_sales_path, 'rb') as f:
        dict_sales = pickle.load(f)
    dict_stocks_path = step2_task_artifacts['dict_stocks'].get_local_copy()
    with open(dict_stocks_path, 'r') as f:
        dict_stocks = json.load(f)
    start_dates_path = step2_task_artifacts['start_dates'].get_local_copy()
    with open(start_dates_path, 'r') as f:
        start_dates = json.load(f)
    end_dates_path = step2_task_artifacts['end_dates'].get_local_copy()
    with open(end_dates_path, 'r') as f:
        end_dates = json.load(f)
    strategy_names_path = step2_task_artifacts['strategy_names'].get_local_copy()
    # read as str from txt
    with open(strategy_names_path, 'r') as f:
        strategy_names = f.read()

    # the keys in dict_deliveries_from_warehouse and dict_arrivals_store_deliveries are str dates. i want stay just the keys that are beteen
    dict_deliveries_from_warehouse = {k: v for k, v in dict_deliveries_from_warehouse.items() if
                                      k >= start_date and k <= end_date}
    dict_arrivals_store_deliveries = {k: v for k, v in dict_arrivals_store_deliveries.items() if
                                      k >= start_date and k <= end_date}

    # in dict_deliveries_from_warehouse and dict_arrivals_store_deliveries after str date keys there is list of sku. i want
    # delete skus from these lists if they not in relevant_skus_to_this_machine

    print("dict_deliveries_from_warehouse2.keys(): ", dict_deliveries_from_warehouse.keys())
    print("dict_arrivals_store_deliveries2.keys(): ", dict_arrivals_store_deliveries.keys())


    def filter_skus(dictionary, relevant_skus):
        return {date: [str(sku) for sku in skus if str(sku) in relevant_skus] for date, skus in dictionary.items()}


    # Filter SKUs for both dictionaries
    filtered_deliveries_from_warehouse = filter_skus(dict_deliveries_from_warehouse, skus_simulation)
    filtered_arrivals_store_deliveries = filter_skus(dict_arrivals_store_deliveries, skus_simulation)
    print("-----------------------------------Phase 3 - tests for inputs dicts-----------------------------------")



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

    print("-----------------------------------Phase 4 - start strategy-----------------------------------")
    all_results_naive_bayes = main_simulation(dict_deliveries_from_warehouse=dict_deliveries_from_warehouse,
                    dict_arrivals_store_deliveries=dict_arrivals_store_deliveries,
                    skus_simulation=skus_simulation, dict_sales=dict_sales, dict_stocks=dict_stocks,
                    start_dates=start_dates, end_dates=end_dates
                    , strategy_function=apply_strategy_naive_bayes)
    print("all_results_naive_bayes: ", all_results_naive_bayes)

    print("-----------------------------------Phase 5 - upload final artifacts-----------------------------------")
    task.upload_artifact("all_results_naive_bayes", artifact_object=all_results_naive_bayes)

else:
    print("step2_fashion_strategy_calculation_task_id is empty, empty task")
