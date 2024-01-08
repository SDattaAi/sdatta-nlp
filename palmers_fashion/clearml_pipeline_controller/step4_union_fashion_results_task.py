from clearml import Task


Task.add_requirements("requirements.txt")
task = Task.init(project_name="palmers_fashion", task_name="step4_union_fashion_results_task")
task.set_base_docker("palmerscr.azurecr.io/clean/ubuntu22.04-private-pip:1.0.2")
task.set_user_properties()
task.set_repo(repo='git@github.com:SDattaAi/sdatta-nlp.git', branch='oran-branch')
task.execute_remotely('ultra-high-cpu')
task.add_tags(['important'])
args = {
    "step3_fashion_strategy_calculation_task_ids": []
}
task.connect(args)
print('Arguments: {}'.format(args))
step3_fashion_strategy_calculation_task_ids = args["step3_fashion_strategy_calculation_task_ids"]
final_clean_all_results = {}
all_results = {}
for task_id in step3_fashion_strategy_calculation_task_ids:
    print("id_of_task", task_id)
    task_id = Task.get_task(task_id=task_id)
    print("task.artifacts", task.artifacts)
    # dict
    print("final_clean_results loading")
    # dict
    # final_clean_results_path = task_id.artifacts['final_clean_results'].get_local_copy()
    # results = task_id.artifacts['results'].get_local_copy()
    # with open(final_clean_results_path, 'r') as f:
    #     final_clean_results_one_task = json.load(f)
    # with open(results, 'r') as f:
    #     results_one_task = json.load(f)



print("-----------------------------------Phase 3 - upload final artifacts-----------------------------------")

# task.upload_artifact("final_clean_all_results_df", final_clean_all_results_df, wait_on_upload=True)
# task.upload_artifact("final_clean_all_results_dict", final_clean_all_results, wait_on_upload=True)
# task.upload_artifact("all_results", all_results, wait_on_upload=True)
