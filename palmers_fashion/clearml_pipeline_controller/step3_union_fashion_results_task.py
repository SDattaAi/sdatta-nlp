from clearml import Task
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pytz

Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers/training", task_name="step2_union_fashion_results_task")
task.set_base_docker("palmerscr.azurecr.io/clean/ubuntu22.04-private-pip:1.0.2")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta_packages_new.git', branch='oran-brach')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['important'])
args = {
    "ids_of_task": []
}
task.connect(args)
print('Arguments: {}'.format(args))
ids_of_task = args["ids_of_task"]
final_clean_all_results = {}
all_results = {}
for id_of_task in ids_of_task:
    print("id_of_task", id_of_task)
    task_id = Task.get_task(task_id=id_of_task)
 #   print("task.artifacts", task.artifacts)
    # dict
    print("final_clean_results loading")
    # dict
    # final_clean_results_path = task_id.artifacts['final_clean_results'].get_local_copy()
    # results = task_id.artifacts['results'].get_local_copy()
    # with open(final_clean_results_path, 'r') as f:
    #     final_clean_results_one_task = json.load(f)
    # with open(results, 'r') as f:
    #     results_one_task = json.load(f)



    print("-----------------------------------Phase 3 - upload tables-----------------------------------")

    # task.upload_artifact("final_clean_all_results_df", final_clean_all_results_df, wait_on_upload=True)
    # task.upload_artifact("final_clean_all_results_dict", final_clean_all_results, wait_on_upload=True)
    # task.upload_artifact("all_results", all_results, wait_on_upload=True)
