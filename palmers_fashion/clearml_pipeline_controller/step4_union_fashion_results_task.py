from clearml import Task
from datetime import datetime, timedelta
import pickle


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
for task_id in step3_fashion_strategy_calculation_task_ids:
    print("id_of_task", task_id)

    # Get the task object
    task = Task.get_task(task_id=task_id)

    # Iterating through each date
    current_date = start_date
    while current_date <= end_date:
        date_ = current_date.strftime("%Y-%m-%d").replace("-", "_")

        # Check if date_ is contained in any of the artifact keys
        for key in task.artifacts.keys():
            if date_ in key:
                # Code to read the pickle file and update for this date
                artifact = task.artifacts[key].get()
                with open(artifact, 'rb') as f:
                    data = pickle.load(f)
                    if current_date not in final_all_results:
                        final_all_results[current_date] = data
                    else:
                        final_all_results[current_date].update(data)
                break  # Break the loop once the matching artifact is found

        if current_date not in final_all_results:
            final_all_results[current_date] = {}

        current_date += timedelta(days=1)  # Move to the next date



print("-----------------------------------Phase 3 - upload final artifacts-----------------------------------")

# task.upload_artifact("final_clean_all_results_df", final_clean_all_results_df, wait_on_upload=True)
# task.upload_artifact("final_clean_all_results_dict", final_clean_all_results, wait_on_upload=True)
# task.upload_artifact("all_results", all_results, wait_on_upload=True)
