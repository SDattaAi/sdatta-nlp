
import numpy as np
import pandas as pd
from config_google_trend_and_mapping import *
from typing import  Tuple, Optional, List


def store_location_load(path: str) -> pd.DataFrame:
    """
    Loads the store location data from a CSV file at the given path, and returns it as a pandas DataFrame.

    Args:
        path (str): The file path of the CSV file containing the store location data.

    Returns:
        pd.DataFrame: The store location data as a pandas DataFrame.
    """
    store_location_df = pd.read_csv(path)
    if "Unnamed: 0" in store_location_df.columns:
        store_location_df = store_location_df.drop(columns="Unnamed: 0", axis=1)
    return store_location_df

def filter_data_with_country(store_location_df: pd.DataFrame, country_str: str, country_chose: str, latitude_str: str, longitude_str: str) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Filters the store location data by a specific country and returns the filtered data as well as an array of unique store IDs in the country.

    Args:
        store_location_df (pd.DataFrame): DataFrame containing store location data.
        country_str (str): Name of the column in `store_location_df` that contains the country names.
        country_chose (str): Name of the country to filter by.
        latitude_str (str): Name of the column to be used for latitude information.
        longitude_str (str): Name of the column to be used for longitude information.

    Returns:
        Tuple[pd.DataFrame, np.ndarray]: A tuple containing two items - the filtered store location data as a DataFrame and an array of unique store IDs in the country.
    """
    data = store_location_df[store_location_df[country_str] == country_chose]
    unique_stores = store_location_df[store_location_df[country_str] == country_chose]["store_id"].unique()
    return data, unique_stores


def map_function(store_id: int, outlets_sdatta: List[int] = OUTLETS_SDATTA, outlets_palmers: List[int] = OUTLETS_PALMERS) -> Optional[str]:
    """
    Map a given store ID to its corresponding chain name ('sdatta' or 'palmers').

    Args:
        store_id (int): The store ID to be mapped.
        outlets_sdatta (List[int], optional): A list of store IDs for sdatta outlets. Defaults to OUTLETS_SDATTA.
        outlets_palmers (List[int], optional): A list of store IDs for Palmers outlets. Defaults to OUTLETS_PALMERS.

    Returns:
        Optional[str]: The name of the chain that the store belongs to ('sdatta' or 'palmers') or None if the store ID is not found in either of the lists.

    """
    if store_id in outlets_sdatta:
        return 'sdatta'
    elif store_id in outlets_palmers:
        return 'palmers'
    else:
        return None

def load_data(path: str, date_column_name: str, sku_column_name: str, store_column_name: str, end_date: str, sort_by_date: bool = False) -> pd.DataFrame:

    """
    Load data from a csv file.

    Args:
        end_date:
        date_column_name:   Name of the date column in the data.
        path: Path to the csv file.
        sku_column_name: Name of the SKU column in the data.
        store_column_name: Name of the store column in the data.

    Returns:
        A pandas DataFrame containing the loaded data.

    Note:
        The data is loaded from a csv file, dropped of an 'Unnamed: 0' column if present,
        and filtered to contain only data with a date less than the specified END_DATE.
        The date column is converted to datetime format.
        The SKU and store columns are converted to categorical data.
        The data is grouped by SKU and date and summarized to keep only the sum of sales.
    """
    data = pd.read_csv(path)
    if "Unnamed: 0" in data.columns:
        data = data.drop("Unnamed: 0", axis=1)
    if set(['outlet', 'mat_no', 'quantity']).issubset(set(data.columns)):
        data = data[['date', 'outlet', 'mat_no', 'quantity']].rename(
            columns={'outlet': 'store', "mat_no": 'sku', 'quantity': "sales"})
    if sort_by_date:
        data = data[data[date_column_name] < end_date]
    data[date_column_name] = pd.to_datetime(data[date_column_name])
    data[sku_column_name] = data[sku_column_name].astype('category')
    data[store_column_name] = data[store_column_name].astype('category')
    return data


def expand_data_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expend the data by date.

    Args:
        df: The dataframe to expend.

    Returns:
        The expended dataframe.

    *Note:
        Dataframe must have columns: store, item, date, sales.
    """
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df['day'] = df.index.day
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day_of_week'] = df.index.dayofweek
    df['day_of_year'] = df.index.dayofyear
    df['day_of_year'] = df.index.dayofyear
    df['name_of_day'] =  df.index.strftime("%A")
    df['week_of_year'] = df.index.isocalendar().week
    df["week_of_year"] = df["week_of_year"].apply(int)
    df['quarter'] = df.index.quarter
    df['day_of_the_month'] = df.index.days_in_month
    df['is_weekend_c'] = df['day_of_week'].apply(lambda x: 1 if x in [5, 6] else 0)
    df['is_weekend_j'] = df['day_of_week'].apply(lambda x: 1 if x in [4, 5] else 0)
    return df