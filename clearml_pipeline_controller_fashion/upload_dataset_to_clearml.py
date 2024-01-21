# create example dataset
from clearml import StorageManager, Dataset

# Download sample csv file
csv_file = '/palmers_fashion/clearml_pipeline_controller_fashion/max_stock_date_is_first_date_skus.csv'

# Create a dataset with ClearML`s Dataset class
dataset = Dataset.create(
    dataset_project="palmers_fashion", dataset_name="max_stock_date_is_first_date_skus"
)

# add the example csv
dataset.add_files(path=csv_file)

# Upload dataset to ClearML server (customizable)
dataset.upload()

# commit dataset changes
dataset.finalize()