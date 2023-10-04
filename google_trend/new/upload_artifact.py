from clearml import Task
# init the task name and project name and clone the task. the task object will be used to upload the artifacts and read it
import pickle
import pandas as pd

task = Task.init(project_name="examples", task_name="all_queries_results_google_trends")
with open('all_queries_results.pkl', 'rb') as f:
    all_queries_results = pickle.load(f)
df_of_all_items_and_there_descriptions = pd.read_csv('df_of_all_items_and_there_descriptions_1.csv')
task.upload_artifact(artifact_object=all_queries_results, name='all_queries_results_google_trends')
task.upload_artifact(artifact_object=df_of_all_items_and_there_descriptions, name='df_of_all_items_and_there_descriptions')