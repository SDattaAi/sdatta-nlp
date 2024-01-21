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
    "step3_fashion_strategy_calculation_task_ids": ['846ca60976a14fb0bde16266c35f59d5',
                                                    'd2de6bb885f6422dbc81201707a5899b',
                                                    '1cb12f808af7460d95cbc8829c8ee14d',
                                                    'df61329d2c914d6a969049bd7ad1095e',
                                                    'eb1f2efe5c2a45c7a0b04178ad16e2c2',
                                                    'b45d50455ec549219a76443a71f478fc',
                                                    '24c4fef7f05f43af8518fdf2ba37084c',
                                                    '5e115298f4d04ae89bd38f7ba28267c2',
                                                    '6af5d9cd0c2f4946b3e41ba50ec21091',
                                                    'c7d53036e30d4fcbb988b104ac10f140'],
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
all_results_naive_bayes_all_tasks = {}
for task_id in step3_fashion_strategy_calculation_task_ids:
    print("id_of_task", task_id)

    # Get the task object
    if "all_results_naive_bayes" in Task.get_task(task_id=task_id).artifacts.keys():
        all_results_path = Task.get_task(task_id=task_id).artifacts['all_results_naive_bayes'].get_local_copy()
        with open(all_results_path, 'r') as f:
            all_results = json.load(f)
        for date in all_results:
            print("date:", date)
            if date in all_results:
                if date not in all_results_naive_bayes_all_tasks:
                    all_results_naive_bayes_all_tasks[date] = {}
                all_results_naive_bayes_all_tasks[date].update(all_results[date].copy())






print("-----------------------------------Phase 3 - upload final artifacts-----------------------------------")
if all_results_naive_bayes_all_tasks != {}:
    print("all_results_naive_bayes_all_tasks", all_results_naive_bayes_all_tasks)
    task.upload_artifact("all_results_naive_bayes_all_tasks", all_results_naive_bayes_all_tasks, wait_on_upload=True)

