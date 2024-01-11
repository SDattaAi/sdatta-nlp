import json
import pickle

from clearml import Task

from sdatta_learn.fashion_strategy.simulation.naive_bayes_benchmark.simulation_with_benchmark import main_simulation_benchmark

Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step3_fashion_strategy_calculation_task")
task.set_base_docker("palmerscr.azurecr.io/clean/ubuntu22.04-private-pip:1.0.2")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
#task.execute_remotely('ultra-high-cpu')
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
    "step2_fashion_strategy_calculation_task_id": "e14df6dfa23b44d69c824007dcb78812",
    "start_date": '2021-08-01',
    "end_date":  '2023-12-01',
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
    print("dict_arrivals_store_deliveries: ", dict_arrivals_store_deliveries)
    print("dict_deliveries_from_warehouse: ", dict_deliveries_from_warehouse)
    print("stores_simulation: ", stores_simulation)
    print("skus_simulation: ", skus_simulation)
    print("dict_sales: ", dict_sales)
    print("dict_stocks: ", dict_stocks)
    print("start_dates: ", start_dates)
    print("end_dates: ", end_dates)
    print("strategy_names: ", strategy_names)


    print("-----------------------------------Phase 3 - start strategy-----------------------------------")
    main_simulation_benchmark(dict_arrivals_store_deliveries=dict_arrivals_store_deliveries,
                                dict_deliveries_from_warehouse=dict_deliveries_from_warehouse,
                                skus_simulation=skus_simulation,
                                dict_sales=dict_sales,
                                dict_stocks=dict_stocks,
                                start_dates=start_dates,
                                end_dates=end_dates,
                                clearml_task=None,
                                base_path="")






    print("-----------------------------------Phase 4 - upload final artifacts-----------------------------------")



else:
    print("step2_fashion_strategy_calculation_task_id is empty, empty task")