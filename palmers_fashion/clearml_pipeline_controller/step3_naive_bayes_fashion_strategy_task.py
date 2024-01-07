from clearml import Task


Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step3_naive_bayes_fashion_strategy_task")
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
    "start_dates": "2018-01-01",
    "end_dates": "2023-12-23",
    "strategy_names": "naive_bayes",
    "step2_fashion_strategy_calculation_task_id": "",
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

print("-----------------------------------Phase 2 - strategy-----------------------------------")
if step2_fashion_strategy_calculation_task_id != "":
    print("step2_fashion_strategy_calculation_task_id is not empty, start strategy")
    step2_task = Task.get_task(task_id=step2_fashion_strategy_calculation_task_id)

    print("-----------------------------------Phase 3 - upload final artifacts-----------------------------------")



else:
    print("step2_fashion_strategy_calculation_task_id is empty, empty task")