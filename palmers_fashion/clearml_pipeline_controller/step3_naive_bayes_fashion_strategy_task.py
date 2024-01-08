from clearml import Task
import json
import pickle
from naive_bayes_strategy import main_simulation

Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step3_naive_bayes_fashion_strategy_task")
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
    "start_dates": "2018-01-01",
    "end_dates": "2023-12-23",
    "strategy_names": "naive_bayes",
    "step2_fashion_strategy_calculation_task_id": "8fb6340ee77242eaa453bf788f969d73",
}
print("-----------------------------------Phase 1 - update args-----------------------------------")

task.connect(args)
print('Arguments: {}'.format(args))
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
    step2_task = Task.get_task(task_id=step2_fashion_strategy_calculation_task_id)
    step2_task_artifacts = step2_task.artifacts
    print("step2_task_artifacts: ", step2_task_artifacts)
    # task.upload_artifact('dict_deliveries_from_warehouse', artifact_object=dict_deliveries_from_warehouse)
    # task.upload_artifact('dict_arrivals_store_deliveries', artifact_object=dict_arrivals_store_deliveries)
    # task.upload_artifact('stores_simulation', artifact_object=stores_simulation)
    # task.upload_artifact('skus_simulation', artifact_object=skus_simulation)
    # task.upload_artifact('dict_sales', artifact_object=dict_sales)
    # task.upload_artifact('dict_stocks', artifact_object=dict_stocks)
    # task.upload_artifact('start_dates', artifact_object=start_dates)
    # task.upload_artifact('end_dates', artifact_object=end_dates)
    # task.upload_artifact('strategy_names', artifact_object=strategy_names)
    dict_deliveries_from_warehouse_path = step2_task_artifacts['dict_deliveries_from_warehouse'].get_local_copy()
    # json read
    with open(dict_deliveries_from_warehouse_path, 'r') as f:
        dict_deliveries_from_warehouse = json.load(f)
    print("dict_deliveries_from_warehouse: ", dict_deliveries_from_warehouse)
    dict_arrivals_store_deliveries_path = step2_task_artifacts['dict_arrivals_store_deliveries'].get_local_copy()
    with open(dict_arrivals_store_deliveries_path, 'r') as f:
        dict_arrivals_store_deliveries = json.load(f)
    print("dict_arrivals_store_deliveries: ", dict_arrivals_store_deliveries)
    stores_simulation_path = step2_task_artifacts['stores_simulation'].get_local_copy()
    with open(stores_simulation_path, 'rb') as f:
        stores_simulation = pickle.load(f)
    print("stores_simulation: ", stores_simulation)
    skus_simulation_path = step2_task_artifacts['skus_simulation'].get_local_copy()
    with open(skus_simulation_path, 'rb') as f:
        skus_simulation = pickle.load(f)
    print("skus_simulation: ", skus_simulation)
    dict_sales_path = step2_task_artifacts['dict_sales'].get_local_copy()
    with open(dict_sales_path, 'rb') as f:
        dict_sales = pickle.load(f)
    print("dict_sales: ", dict_sales)
    dict_stocks_path = step2_task_artifacts['dict_stocks'].get_local_copy()
    with open(dict_stocks_path, 'rb') as f:
        dict_stocks = pickle.load(f)
    print("dict_stocks: ", dict_stocks)
    start_dates_path = step2_task_artifacts['start_dates'].get_local_copy()
    with open(start_dates_path, 'rb') as f:
        start_dates = pickle.load(f)
    print("start_dates: ", start_dates)
    end_dates_path = step2_task_artifacts['end_dates'].get_local_copy()
    with open(end_dates_path, 'rb') as f:
        end_dates = pickle.load(f)
    print("end_dates: ", end_dates)
    strategy_names_path = step2_task_artifacts['strategy_names'].get_local_copy()
    # read as str from txt
    with open(strategy_names_path, 'r') as f:
        strategy_names = f.read()

    print("-----------------------------------Phase 3 - start strategy-----------------------------------")
    main_simulation(dict_arrivals_store_deliveries=dict_arrivals_store_deliveries,
                    dict_deliveries_from_warehouse=dict_deliveries_from_warehouse,
                    stores_simulation=stores_simulation,
                    skus_simulation=skus_simulation,
                    dict_sales=dict_sales,
                    dict_stocks=dict_stocks,
                    start_dates=start_dates,
                    end_dates=end_dates,
                    strategy_names=strategy_names)


    print("-----------------------------------Phase 4 - upload final artifacts-----------------------------------")



else:
    print("step2_fashion_strategy_calculation_task_id is empty, empty task")