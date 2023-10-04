from geopy.geocoders import Nominatim
from nltk.util import ngrams
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.corpus import wordnet
import re
import datetime




def get_iso_code_from_lat_and_long(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)

    if location is not None:
        address = location.raw.get('address', {})
        for key in address.keys():
            if "ISO" in key:

                iso_code = address[key]
                return iso_code
        return None

    return None



def map_country_iso_to_none_iso_codes(store_location_df, country_mapping):
    store_location_df.loc[store_location_df['iso_code'].isnull(), 'iso_code'] = store_location_df['country'].map(country_mapping)
    return store_location_df





def item_description_fix_tokens(items_description_df, relevant_column):
    # Lowercase the descriptions
    items_description_df[relevant_column] = items_description_df[relevant_column].str.lower()

    items_description_df[relevant_column] = items_description_df[relevant_column].str.replace('-', ' ')
    # Remove special characters
    items_description_df[relevant_column] = items_description_df[relevant_column].str.replace('[^\w\s]', ' ', regex=True)

    # Remove extra whitespaces
    items_description_df[relevant_column] = items_description_df[relevant_column].str.strip()

    items_description_df[relevant_column] = items_description_df[relevant_column].str.replace('\s+', ' ', regex=True)

    return items_description_df




def generate_word_combinations(sentence, lowest_words, highest_words):
    words = sentence.lower().split()
    result = []

    for n in range(lowest_words, highest_words + 1):
        n_grams = ngrams(words, n)
        combinations = [' '.join(gram) for gram in n_grams]
        result.extend(combinations)

    return result




def get_google_trends_df(interest_over_time):
    timeline_data = interest_over_time['timeline_data']
    # Extract lists of dates, timestamps and values
    dates = [d['date'] for d in timeline_data]
    timestamps = [d['timestamp'] for d in timeline_data]
    values = [d['values'] for d in timeline_data]
    import re


    pattern = re.compile(r'\u2009')

    cleaned_dates = []

    for str in dates:
        cleaned = pattern.sub('', str)
        cleaned_dates.append(cleaned)
    df = pd.DataFrame()
    for list_ in values:
        dict_to_df = {}
        for dict_ in list_:
            query = dict_['query']
            value = dict_['value']
            dict_to_df[query] = value
        df = df.append(dict_to_df, ignore_index=True)
    df['date'] =     cleaned_dates
    for col in df.columns.tolist():
        if col != 'date':
            df[col] = df[col].astype(int)
    return df



def get_product_info(url):
    response = requests.get(url)
    response.raise_for_status()  # Make sure we got a good response

    soup = BeautifulSoup(response.text, 'html.parser')

    description_selector = 'div.value[itemprop="description"]'
    description = soup.select_one(description_selector).get_text(strip=True)

    product_name_selector = 'h1.page-title > span'
    product_name_spans = soup.select(product_name_selector)
    product_name = " ".join([span.get_text(strip=True) for span in product_name_spans])

    return product_name, description




def lemmatize_column(df, column_name):
    lemmatizer = WordNetLemmatizer()
    """Function to apply lemmatization to a column in a pandas DataFrame."""
    # Make sure the column exists in the DataFrame
    if column_name in df.columns:
        # Apply the lemmatizer to each word in each row of the column
        df[column_name] = df[column_name].apply(lambda row: " ".join([lemmatizer.lemmatize(word) for word in word_tokenize(row)]))
    else:
        print(f"The column '{column_name}' is not in the DataFrame.")
    return df





def remove_stopwords(df, column_name):
    stop_words = set(stopwords.words('english'))

    """Function to remove English stopwords from a column in a pandas DataFrame."""
    # Make sure the column exists in the DataFrame
    if column_name in df.columns:
        # Remove stopwords from each row of the column
        df[column_name] = df[column_name].apply(lambda row: " ".join([word for word in word_tokenize(row) if word not in stop_words]))
    else:
        print(f"The column '{column_name}' is not in the DataFrame.")
    return df




def has_meaning(word):
    english_words = set(words.words())

    return word.lower() in english_words and bool(wordnet.synsets(word))

def remove_non_english_words_from_column(df, column_name):
    def remove_non_english_words(text):
        words_list = text.split()
        english_words_list = [word for word in words_list if has_meaning(word)]
        return ' '.join(english_words_list)

    df_copy = df.copy()
    df_copy[column_name] = df_copy[column_name].apply(remove_non_english_words)
    return df_copy

def remove_numbers(df, column_name):
    df[column_name] = df[column_name].str.replace('\d+', '')
    return df

def hierarchical_category_tree_from_text_to_list(input_string):
    # Convert the string to a list using the split() method
    categories_list = re.split(r'\s*(?:->|>)\s*', input_string)
    return categories_list

def from_results_query_to_time_series_df_google_trend(results):
    interest_over_time = results["interest_over_time"]
    timeline_data = interest_over_time['timeline_data']
    dates = [d['date'] for d in timeline_data]
    #timestamps = [d['timestamp'] for d in timeline_data]
    values = [d['values'] for d in timeline_data]
    pattern = re.compile(r'\u2009')
    cleaned_dates = []
    for str in dates:
        cleaned = pattern.sub('', str)
        cleaned_dates.append(cleaned)
    df = pd.DataFrame()
    for list_ in values:
        dict_to_df = {}
        for dict_ in list_:
            query = dict_['query']
            value = dict_['value']
            dict_to_df[query] = value
        new_df = pd.DataFrame([dict_to_df])
        df = pd.concat([df, new_df], ignore_index=True)
    df['date'] = cleaned_dates
    return df



def from_sting_dates_google_trends_to_fix_datetime_range(date_ranges):
    formatted_dates = []
    for date_range in date_ranges:
        terms_list = re.split('–|, ', date_range)
        if len(terms_list) != 4:
            # Check the scenario based on the number of parts in end_date_parts
            if len(terms_list[1]) < 3:
                # Scenario 1: month day1-day2, year
                year = int(terms_list[2])
                month = datetime.datetime.strptime(terms_list[0].split(' ')[0], '%b').month
                day = int(terms_list[1])
            else:
                # Scenario 2: month1 day1-month2 num2, year
                year = int(terms_list[2])
                month = datetime.datetime.strptime(terms_list[1].split(" ")[0], '%b').month
                day = int(terms_list[1].split(" ")[1])
        else:
            # Scenario 3: month1 day1, year1 - month2 day2, year2
            year = int(terms_list[3])
            month = datetime.datetime.strptime(terms_list[2].split(' ')[0], '%b').month
            day = int(terms_list[2].split(' ')[1])
        formatted_date = datetime.datetime(year, month, day).strftime('%Y-%m-%d')
        formatted_dates.append(formatted_date)
    return formatted_dates