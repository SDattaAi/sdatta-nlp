import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from config_google_trend_and_mapping import *
from typing import Tuple, Union
def calculate_2021_sales_by_store(exp_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculates the total sales in 2021 for each store in the given dataset, as well as the total sales per store for each year.

        Args:
            exp_data (pd.DataFrame): A pandas dataframe containing the experimental data.

        Returns:
            A tuple containing two pandas dataframes:
            1. A dataframe with the total sales in 2021 for each store, with columns "store_id" and "2021_sales".
            2. A dataframe with the total sales per store for each year, with columns "store", "year", and "sales".
        """
        sum_of_sales_in_years = exp_data.groupby(["store", "year"]).sum()["sales"].reset_index()
        sum_of_sales_in_2021 = sum_of_sales_in_years[sum_of_sales_in_years["year"] == 2021][["store", "sales"]]
        sum_of_sales_in_2021 = sum_of_sales_in_2021.rename(columns={"store": "store_id", "sales": "2021_sales"})
        return sum_of_sales_in_2021, sum_of_sales_in_years

def get_relevant_stores_info(sum_of_sales_in_years: pd.DataFrame, l_outlet_v_PATH: str) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Retrieves information about relevant stores from the provided sales data and the L_OUTLET_V file.

    Args:
        sum_of_sales_in_years (pd.DataFrame): Sales data grouped by store and year.
        l_outlet_v_PATH (str): Path to the L_OUTLET_V file.

    Returns:
        Tuple[np.ndarray, pd.DataFrame]: A tuple containing an array of relevant store IDs and a DataFrame with information
        about these stores, including their names, IDs, and countries.
    """
    our_relevant_stores = sum_of_sales_in_years["store"].unique()
    l_outlet_v = pd.read_csv(l_outlet_v_PATH)
    l_outlet_v = l_outlet_v[["Outlet Stufe 01 (DESC form)", "20PLANT", "Land Stufe 01 (DESC form)"]].dropna()
    l_outlet_v = l_outlet_v.rename(columns={"Outlet Stufe 01 (DESC form)": "store_name", "20PLANT": "store_id", "Land Stufe 01 (DESC form)": "country"})
    return our_relevant_stores, l_outlet_v

def find_missing_stores(our_relevant_stores: list, l_outlet_v: pd.DataFrame) -> list:
    """
    Find stores in our_relevant_stores that are missing in l_outlet_v.

    Args:
        our_relevant_stores: A list of relevant store IDs.
        l_outlet_v: A DataFrame containing the store information.

    Returns:
        A list of store IDs that are missing in l_outlet_v.
    """
    missing_store = []
    for store_id in our_relevant_stores:
         if store_id in l_outlet_v["store_id"].to_list():
           pass
         else:
             missing_store.append(store_id)
    return missing_store

def merge_and_clean_relevant_stores_info(our_relevant_stores: pd.DataFrame, l_outlet_v: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the relevant stores with store location data and cleans the resulting dataframe.

    Args:
        our_relevant_stores (pd.DataFrame): A pandas dataframe containing the relevant stores.
        l_outlet_v (pd.DataFrame): A pandas dataframe containing the store location data.

    Returns:
        pd.DataFrame: A cleaned pandas dataframe containing the merged store information.
    """
    our_relevant_stores = pd.DataFrame(our_relevant_stores, columns=["store_id"])
    merged_df = pd.merge(our_relevant_stores, l_outlet_v, how="left", on='store_id')
    merged_df = merged_df.dropna()
    merged_df["store_name + country"] = merged_df["store_name"] + " " + merged_df["country"]

    return  merged_df


def get_location(store_country):
    """
    Returns the location of a store given its country.

    Args:
    store_country (str): Country of the store

    Returns:
    str: Location of the store
    """
    return DIRECT_LOCATIONS.get(store_country, np.nan)

def add_specific_location(our_relevant_stores):
    """
    Adds a new column to the input DataFrame with the specific location of each store.

    Args:
    - our_relevant_stores: A DataFrame with the relevant stores information, including a column called "store_name + country".

    Returns:
    - A copy of the input DataFrame with a new column called "specific_location".
    """
    our_relevant_stores['spesipic_location'] = our_relevant_stores['store_name + country'].apply(get_location)
    return our_relevant_stores

def get_lat_and_long_from_location(store_name: str) -> Union[Tuple[float, float], None]:
    """
    Get the latitude and longitude of a store location using its name.

    Args:
        store_name (str): The name of the store location.

    Returns:
        Union[Tuple[float, float], None]: A tuple containing the latitude and longitude of the store location,
        or None if the location could not be found.
    """
    geolocator = Nominatim(user_agent="oran_nahum_1_sdatta")
    location = geolocator.geocode(store_name)
    if location is None:
        return None
    return location.latitude, location.longitude

def merge_relevant_store_location_and_sales_data(our_relevant_stores: pd.DataFrame, sum_of_sales_in_2021: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the relevant stores' location information with the sales data for 2021.

    Args:
    - our_relevant_stores: A pandas DataFrame that contains the relevant stores' information.
    - sum_of_sales_in_2021: A pandas DataFrame that contains the sum of sales data for 2021.

    Returns:
    - A pandas DataFrame that contains the merged data.
    """
    our_relevant_stores[['latitude', 'longitude']] = our_relevant_stores['spesipic_location'].apply(lambda x: pd.Series(get_lat_and_long_from_location(x) if get_lat_and_long_from_location(x) is not None else [None, None]))
    merged_df = our_relevant_stores.merge(sum_of_sales_in_2021, how="left", on='store_id')
    return merged_df