


from clearml.automation import PipelineController

number_of_machines = 10
start_date = '2023-01-01'
end_date = '2023-12-01'
relevant_stores = ['76', '4134', '4904', '10', '100', '109', '11', '117', '133', '135', '141', '143', '164', '181'
    , '183', '185', '201', '213', '214', '22', '3005', '3202', '4104', '4123', '4129', '42', '45', '46', '4803', '4906'
    , '5', '67', '68', '7', '73', '8', '82', '88', '89', '104', '174', '3208', '37', '63', '91', '96', '202', '21', '90'
    , '95', '121', '144', '147', '173', '4133', '47', '81', '170', '28', '172', '15', '166', '217', '27', '4', '51'
    , '114', '122', '160', '3', '69', '182', '26', '105', '106', '119', '130', '136', '149', '150', '156', '159'
    , '162', '167', '168', '171', '179', '18', '180', '184', '186', '189', '203', '215', '218', '220', '221', '225'
    , '29', '44', '4805', '50', '52', '55', '56', '61', '64', '74', '79', '84', '85', '99', '152', '163', '175', '216'
    , '219', '3245', '57', '3205', '43', '226', '35', '36', '123', '188']


if 'VZ01' not in relevant_stores:
     relevant_stores.append('VZ01')
controller = PipelineController(project="palmers_fashion",
                                name=f'palmers_fashion_strategy_pipeline_controller',
                                docker="palmerscr.azurecr.io/clean/nvidia-cuda_11.0.3-cudnn8-runtime-ubuntu20.04:1.0.1-private",
                                repo='git@github.com:SDattaAi/sdatta-nlp.git',
                                repo_branch='oran-branch')


controller.add_step(name="step1_load_all_relevant_data_for_fashion",
                    base_task_project="palmers_fashion",
                    base_task_name="step1_load_all_relevant_data_for_fashion_task",
                    parameter_override={"General/relevant_stores": relevant_stores,
                                        'General/start_date': start_date,
                                        'General/end_date': end_date,
                                        'General/number_of_machines': number_of_machines},
                    execution_queue="ultra-high-cpu")


fashion_strategy_preparation_dicts_nodes = []
fashion_strategy_calculation_nodes = []
for number_of_machine in range(number_of_machines):
    fashion_strategy_preparation_dicts_node_name = f"step2_fashion_strategy_preparation_dicts_{number_of_machine}"
    controller.add_step(name=fashion_strategy_preparation_dicts_node_name,
                        base_task_project="palmers_fashion",  #####sales_filled_table_name
                        base_task_name="step2_fashion_strategy_preparation_dicts_task",
                        parents=[f"step1_load_all_relevant_data_for_fashion"],
                        parameter_override={"General/number_of_this_machine": number_of_machine,
                                            'General/start_date': start_date,
                                            'General/end_date': end_date,
                                            'General/relevant_stores': relevant_stores,
                                            'General/step1_load_all_relevant_data_for_fashion_task_id': '${step1_load_all_relevant_data_for_fashion.id}'},
                        execution_queue="ultra-high-cpu")
    fashion_strategy_preparation_dicts_nodes.append(fashion_strategy_preparation_dicts_node_name)
    fashion_strategy_calculation_node_name = f"step3_fashion_strategy_calculation_{number_of_machine}"
    controller.add_step(name=fashion_strategy_calculation_node_name,
                        base_task_project="palmers_fashion",
                        base_task_name="step3_fashion_strategy_calculation_task",
                        parents=[fashion_strategy_preparation_dicts_node_name],
                        parameter_override={ 'General/start_date': start_date,
                                            'General/end_date': end_date,
                                             'General/step2_fashion_strategy_calculation_task_id': '${' + fashion_strategy_preparation_dicts_node_name + '.id}'},
                        execution_queue="ultra-high-cpu")
    fashion_strategy_calculation_nodes.append(fashion_strategy_calculation_node_name)

fashion_strategy_calculation_nodes_task_ids = "[" + ", ".join([f"${{{node}.id}}" for node in fashion_strategy_calculation_nodes]) + "]"
controller.add_step(name="step4_union_fashion_results",
                    base_task_project="palmers_fashion",
                    base_task_name="step4_union_fashion_results_task",
                    parents=fashion_strategy_calculation_nodes,
                    parameter_override={'General/step3_fashion_strategy_calculation_task_ids': fashion_strategy_calculation_nodes_task_ids,
                                        'General/start_date': start_date,
                                        'General/end_date': end_date,},
                    execution_queue="ultra-high-cpu")
controller.start()