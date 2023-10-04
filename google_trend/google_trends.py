

import pandas as pd
import numpy as np
import datetime
from pytrends.request import TrendReq
from config_google_trend_and_mapping import lags_array
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from typing import List

def google_trend_word_in_AT_and_DE_regions(store_location_df_sdatta: pd.DataFrame, word: str, AT_REGIONS_NUM: List[int], DE_REGIONS_STR: str) -> pd.DataFrame:
    """
    Retrieves Google Trends data for a given word in Austria and Germany.

    Args:
        store_location_df_sdatta (pd.DataFrame): DataFrame containing the store locations data.
        word (str): The word to retrieve Google Trends data for.
        AT_REGIONS_NUM (List[int]): A list of the region numbers for Austria to retrieve data for.
        DE_REGIONS_STR (str): The string to indicate Germany in the location names.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved Google Trends data.

    """
    store_location_df_sdatta["sub_region"] = np.nan
    df_all_regions = pd.DataFrame()
    ## austria
    for AT_region in AT_REGIONS_NUM:
        df = pd.DataFrame()
        pytrends = TrendReq(hl="de-AT", tz=360)
        kw_list = [word]
        geo = "AT-" + str(AT_region)
        start_date = datetime.date(2018, 1, 1)
        end_date = datetime.date.today()
        timeframe = f"{start_date} {end_date}"
        pytrends.build_payload(kw_list, cat=0, geo=geo, timeframe=timeframe)
        trend_data = pytrends.interest_over_time()
        for lag in lags_array:
            df_all_regions[word + "_" + geo + "_lag" + str(lag) + "W"] = trend_data[kw_list].shift(lag)
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [word]
    geo = "AT"
    start_date = datetime.date(2018, 1, 1)
    end_date = datetime.date.today()
    timeframe = f"{start_date} {end_date}"
    pytrends.build_payload(kw_list, cat=0, geo=geo, timeframe=timeframe)
    trend_data = pytrends.interest_over_time()
    for lag in lags_array:
        df_all_regions[word + "_" + geo + "_lag" + str(lag) + "W"] = trend_data[kw_list].shift(lag)

    ## germany
    for DE_region in DE_REGIONS_STR:
        pytrends = TrendReq(hl="de-DE", tz=360)
        kw_list = [word]
        geo = "DE-" + str(DE_region)
        start_date = datetime.date(2018, 1, 1)
        end_date = datetime.date.today()
        timeframe = f"{start_date} {end_date}"
        pytrends.build_payload(kw_list, cat=0, geo=geo, timeframe=timeframe)
        trend_data = pytrends.interest_over_time()
        for lag in lags_array:
            df_all_regions[word + "_" + geo + "_lag" + str(lag) + "W"] = trend_data[kw_list].shift(lag)
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [word]
    geo = "DE"
    start_date = datetime.date(2018, 1, 1)
    end_date = datetime.date.today()
    timeframe = f"{start_date} {end_date}"
    pytrends.build_payload(kw_list, cat=0, geo=geo, timeframe=timeframe)
    trend_data = pytrends.interest_over_time()
    for lag in lags_array:
        df_all_regions[word + "_" + geo + "_lag" + str(lag) + "W"] = trend_data[kw_list].shift(lag)

    return df_all_regions


def data_loader_germany_with_prices(path: str) -> pd.DataFrame:
    """
    Loads sales data from a CSV file and returns a cleaned DataFrame with relevant columns.

    Args:
        path: A string specifying the file path to the CSV data.

    Returns:
        A pandas DataFrame with columns for the date, store, SKU, sales quantity, discounted total price, total price,
        discounted price, and regular price.

    Raises:
        Any exceptions that may occur during the loading and cleaning of the data.
    """

    data = pd.read_csv(path)
    if "Unnamed: 0" in data.columns:
        data = data.drop("Unnamed: 0", axis=1)
    data['date'] = pd.to_datetime(data['date'])
    data = data[['date', 'outlet', 'mat_no', 'quantity', 'discounted_totalprice', 'totalprice', 'dicounted_price', 'price']].rename(columns={'outlet':'store', "mat_no": 'sku', 'quantity' : "sales"})
    return data

def return_n_large_google_trend_corr(corr_df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """
    Returns a DataFrame with the n largest correlation values and their corresponding index.

    Parameters:
    corr_df (pd.DataFrame): The correlation DataFrame to search through.
    n (int): The number of largest correlation values to return. Default is 20.

    Returns:
    pd.DataFrame: A DataFrame with the n largest correlation values and their corresponding index.
    """
    best_corr_df = pd.DataFrame(columns=["(word-region-lag, store)", "correlation value"])
    for n in range(1, n + 1):
        largest_n_values = corr_df.stack().nlargest(n)
        n_largest_value = largest_n_values.iloc[-1]
        n_largest_value_idx = largest_n_values.index[-1]
        best_corr_df = best_corr_df.append({"(word-region-lag, store)": n_largest_value_idx, "correlation value": n_largest_value}, ignore_index=True)
    return best_corr_df


def preprocess_google_trend(google_trends: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the Google Trends data by performing the following operations:
    - Decomposes the data into trend, seasonal, and residual components using seasonal decomposition
    - Computes the first difference of the data
    - Computes a rolling mean with a window size of 3
    - Computes the lagged version of the data

    Parameters:
    google_trends (pd.DataFrame): The Google Trends data to be preprocessed

    Returns:
    pd.DataFrame: The preprocessed data with the following columns:
        - 'google_trends': The original Google Trends data
        - 'trend': The trend component of the data
        - 'seasonal': The seasonal component of the data
        - 'residual': The residual component of the data
        - 'diff': The first difference of the data
        - 'smooth': The rolling mean with a window size of 3
        - 'lagged': The lagged version of the data
    """
    decomposition = seasonal_decompose(google_trends, model='additive')
    google_trends_trend = decomposition.trend
    google_trends_seasonal = decomposition.seasonal
    google_trends_residual = decomposition.resid
    google_trends_diff = google_trends.diff().dropna()
    google_trends_smooth = google_trends.rolling(window=3).mean()
    google_trends_lagged = google_trends.shift(1)
    preprocessed_data = pd.concat([google_trends, google_trends_trend, google_trends_seasonal, google_trends_residual, google_trends_diff, google_trends_smooth, google_trends_lagged], axis=1)
    preprocessed_data.columns = ['google_trends', 'trend', 'seasonal', 'residual', 'diff', 'smooth', 'lagged']
    preprocessed_data = preprocessed_data.fillna(0)
    return(preprocessed_data)

def calculate_statistical_significance(df: pd.DataFrame, list_of_feat: list[str], target: str) -> list[float]:
    """
    Calculate statistical significance of features.

    Args:
        df: pandas DataFrame
        list_of_feat: list of features
        target: target column

    Returns:
        list of statistical significance of features
    """


    X = df[list_of_feat]
    X = sm.add_constant(X)
    y = df[target]
    model = sm.OLS(y, X).fit()
    return model.pvalues.tolist()