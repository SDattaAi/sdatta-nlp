
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


def add_label_column_and_fill_germany_label(store_location_df: pd.DataFrame, label_str: str, country_str: str,
                                            germany_str: str) -> pd.DataFrame:
    """
    Adds a new label column to the given store_location_df DataFrame and fills it with -1 for stores located in Germany.

    Args:
        store_location_df (pd.DataFrame): The DataFrame containing the store location data.
        label_str (str): The label column name to be added.
        country_str (str): The name of the column containing country information.
        germany_str (str): The string value used to indicate Germany in the country column.

    Returns:
        pd.DataFrame: The updated store_location_df DataFrame.
    """
    store_location_df[label_str] = np.nan
    for index, row in store_location_df.iterrows():
        if row[country_str] == germany_str:
            store_location_df.loc[index, label_str] = -1
    return store_location_df


def cluster_by_latitude_and_longitude(X: pd.DataFrame, n_clusters: int = 7, random_state: int = 0, label_str: str = "label") -> pd.DataFrame:
    """
    Clusters a dataframe by latitude and longitude using KMeans algorithm.

    Args:
        X: The input dataframe.
        n_clusters: The number of clusters to generate (default 7).
        random_state: Determines random number generation for centroid initialization (default 0).
        label_str: The name of the label column to add to the dataframe (default "label").

    Returns:
        A dataframe with the cluster label assigned to each row.
    """

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    kmeans.fit(X.values)
    labels = kmeans.labels_
    for i in range(len(X)):
        X.loc[X.index, label_str] = labels
    return X


def add_cluster_labels_to_store_location_df(X_with_clusters: pd.DataFrame, store_location_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds the cluster labels to the store_location_df DataFrame.
    Args:
        X_with_clusters:    The dataframe containing the cluster labels.
        store_location_df:  The dataframe containing the store location data.

    Returns:    The updated store_location_df DataFrame.

    """
    store_location_df = pd.merge(X_with_clusters[["label", "store"]], store_location_df, left_on="store",
                                 right_on="store_id", how="right")
    store_location_df["label"] = store_location_df["label"].fillna(-1)
    return store_location_df