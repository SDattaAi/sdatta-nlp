import pandas as pd
from clearml import Task
from datetime import datetime, timedelta
import json


Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step4_union_fashion_results_task")
task.set_base_docker("palmerscr.azurecr.io/clean/ubuntu22.04-private-pip:1.0.2")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['important'])
args = {
    "step3_fashion_strategy_calculation_task_ids": [],
    "start_date": '2021-08-01',
    "end_date":  '2023-12-01',
}
task.connect(args)
print('Arguments: {}'.format(args))
start_date = args["start_date"]
end_date = args["end_date"]
step3_fashion_strategy_calculation_task_ids = args["step3_fashion_strategy_calculation_task_ids"]
final_all_results = {}
all_results = {}
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
all_results_all_tasks = {}
for task_id in step3_fashion_strategy_calculation_task_ids:
    print("id_of_task", task_id)

    # Get the task object
    all_results_path = Task.get_task(task_id=task_id).artifacts['all_results'].get_local_copy()
    with open(all_results_path, 'r') as f:
        all_results = json.load(f)
    for date in all_results:
        print("date:", date)
        if date in all_results:
            if date not in all_results_all_tasks:
                all_results_all_tasks[date] = {}
            all_results_all_tasks[date].update(all_results[date].copy())






print("-----------------------------------Phase 3 - upload final artifacts-----------------------------------")
print("all_results_all_tasks", all_results_all_tasks)
task.upload_artifact("all_results_all_tasks", all_results_all_tasks, wait_on_upload=True)

