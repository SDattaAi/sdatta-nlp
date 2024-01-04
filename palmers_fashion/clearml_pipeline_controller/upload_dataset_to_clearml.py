# create example dataset
from clearml import StorageManager, Dataset

# Download sample csv file
csv_file = '/Users/guybasson/Desktop/sdatta-nlp/palmers_fashion/clearml_pipeline_controller/initial_stock_sku_store.csv'

# Create a dataset with ClearML`s Dataset class
dataset = Dataset.create(
    dataset_project="palmers_fashion", dataset_name="initial_stocks"
)

# add the example csv
dataset.add_files(path=csv_file)

# Upload dataset to ClearML server (customizable)
dataset.upload()

# commit dataset changes
dataset.finalize()