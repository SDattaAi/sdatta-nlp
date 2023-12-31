


from clearml.automation import PipelineController
from datetime import datetime, timedelta

number_of_machines = 2
start_date = '2023-12-01'
end_date = '2023-12-23'
relevant_stores = ['51', '100']

# deliver have date from 2018-01-01 to 2023-12-23

if 'VZ01' not in relevant_stores:
     relevant_stores.append('VZ01')
controller = PipelineController(project="palmers_fashion",
                                name=f'palmers_fashion_strategy_pipeline_controller',
                                docker="palmerscr.azurecr.io/clean/nvidia-cuda_11.0.3-cudnn8-runtime-ubuntu20.04:1.0.1-private",
                                repo='git@github.com:SDattaAi/sdatta-nlp.git',
                                repo_branch='oran-brach',
                                add_pipeline_tags=True)


controller.add_step(name="step1_load_all_relevant_data_for_fashion",
                    base_task_project="palmers_fashion",
                    base_task_name="step1_load_all_relevant_data_for_fashion_task",
                    parameter_override={"General/relevant_stores": relevant_stores,
                                        'General/start_date': start_date,
                                        'General/end_date': end_date,
                                        'General/number_of_machines': number_of_machines},
                    execution_queue="ultra-high-cpu",
                    cache_executed_step=True)


fashion_strategy_preparation_dicts_nodes = []
fashion_strategy_calculation_nodes = []
for number_of_machine in range(number_of_machines):
    fashion_strategy_calculation_node_name = f"step2_fashion_strategy_preparation_dicts_{number_of_machine}"
    controller.add_step(name=fashion_strategy_calculation_node_name,
                        base_task_project="palmers_fashion",  #####sales_filled_table_name
                        base_task_name="step2_fashion_strategy_calculation_task",
                        parents=[f"step1_load_all_relevant_data_for_fashion"],
                        parameter_override={"General/number_of_this_machine": number_of_machine,
                                            'General/start_date': start_date,
                                            'General/end_date': end_date,
                                            'General/relevant_stores': relevant_stores,
                                            'General/step1_load_all_relevant_data_for_fashion_task_id': '${step1_load_all_relevant_data_for_fashion.id}'},
                        execution_queue="ultra-high-cpu",
                        cache_executed_step=True)
    fashion_strategy_preparation_dicts_nodes.append(fashion_strategy_calculation_node_name)
    fashion_strategy_calculation_node_name = f"step3_naive_bayes_fashion_strategy_{number_of_machine}"
    controller.add_step(name=fashion_strategy_calculation_node_name,
                        base_task_project="palmers_fashion",
                        base_task_name="step3_naive_bayes_fashion_strategy_task",
                        parents=[fashion_strategy_calculation_node_name],
                        parameter_override={'General/step2_fashion_strategy_calculation_task_id': '${' + fashion_strategy_calculation_node_name + '.id}'},
                        execution_queue="ultra-high-cpu",
                        cache_executed_step=True)
    fashion_strategy_calculation_nodes.append(fashion_strategy_calculation_node_name)



controller.start()