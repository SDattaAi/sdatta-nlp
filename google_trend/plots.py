import folium
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from typing import Dict

def folium_plot(store_location_df: pd.DataFrame,
                latitude_str: str,
                longitude_str: str,
                sdatta_str: str,
                palmers_str: str,
                label_str: str,
                ownership_str: str,
                sales_str_year: str,
                divide_size: float,
                label_colors: Dict[str, str]) -> folium.Map:
    """
    Plots store locations on a Folium map and adds sales data to the markers.

    Args:
    - store_location_df (pd.DataFrame): DataFrame containing store location data
    - latitude_str (str): Name of the column in store_location_df containing latitude data
    - longitude_str (str): Name of the column in store_location_df containing longitude data
    - sdatta_str (str): String representing Sdatta ownership
    - palmers_str (str): String representing Palmers ownership
    - label_str (str): Name of the column in store_location_df containing label data
    - ownership_str (str): Name of the column in store_location_df containing ownership data
    - sales_str_year (str): Name of the column in store_location_df containing sales data for a given year
    - divide_size (float): Divide size for scaling the size of the markers based on sales data
    - label_colors (Dict[str, str]): Dictionary mapping label names to marker colors

    Returns:
    - folium.Map: Folium map object containing the plotted data
    """
    m = folium.Map(location=[store_location_df[latitude_str][0], store_location_df[longitude_str][0]], zoom_start=3)
    sdatta_fg = folium.FeatureGroup(name=sdatta_str)
    palmers_fg = folium.FeatureGroup(name=palmers_str)
    for index, row in store_location_df.iterrows():
        label_color = label_colors[row[label_str]] if row[label_str] in label_colors else 'gray'  # set color based on label
        if row[ownership_str] == sdatta_str:
            folium.CircleMarker(location=[row[latitude_str], row[longitude_str]], radius=row[sales_str_year]/divide_size, color=label_color, fill=True).add_to(sdatta_fg)
        elif row[ownership_str] == palmers_str:
            folium.RegularPolygonMarker(location=[row[latitude_str], row[longitude_str]], number_of_sides=4, radius=row[sales_str_year]/divide_size, color=label_color, fill=True).add_to(palmers_fg)
    sdatta_fg.add_to(m)
    palmers_fg.add_to(m)
    folium.LayerControl().add_to(m)
    return m

def relplot_location_with_label_colors(store_location_df: pd.DataFrame, longitude_str: str, latitude_str: str, label_str: str, sales_str_year: str) -> None:
    """
    Plot store locations on a map with labels colored by a given feature and size of points proportional to sales in a year.

    Args:
    store_location_df (pd.DataFrame): Dataframe containing store locations data.
    longitude_str (str): Column name of longitude data.
    latitude_str (str): Column name of latitude data.
    label_str (str): Column name of label data to be colored.
    sales_str_year (str): Column name of sales data to determine size of points.

    Returns:
    None
    """
    sns.relplot(x=longitude_str, y=latitude_str, hue=label_str, size=sales_str_year,
            sizes=(40, 400), alpha=.7, palette="muted",
            height=6, data=store_location_df)
    plt.title("Stores in map with lat and long with store location clusters")


def plot_germany_austria_borders_and_stores(
    store_location_df: pd.DataFrame,
    germany_regions_borders: str,
    austria_regions_borders: str) -> None:
    """
    Function to plot the borders of Germany and Austria along with the locations of Palmers stores in the region, with markers scaled by their 2021 sales.

    Args:

    store_location_df: pandas DataFrame containing store locations and sales data
    germany_regions_borders: file path to the shapefile containing the borders of the German regions
    austria_regions_borders: file path to the shapefile containing the borders of the Austrian regions
    Returns:

    None, displays the plot
    """
    data_germany = gpd.read_file(germany_regions_borders)
    data_austria = gpd.read_file(austria_regions_borders)
    ax = data_austria.plot(color='lightblue', edgecolor='black', linewidth=0.4, figsize=(14,10))
    for idx, row in data_austria.iterrows():
        ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['iso'], ha='center', va='center', color='black', fontsize=8)
    data_germany.plot(ax=ax, color='yellow', edgecolor='black', linewidth=0.4)
    for idx, row in data_germany.iterrows():
        ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['iso'], ha='center', va='center', color='black', fontsize=8)
    plt.text(11, 53, 'Germany', fontsize=12, color='black', ha='center', va='center')
    plt.text(13.5, 47.7, 'Austria', fontsize=12, color='black', ha='center', va='center')
    store_location_gdf = gpd.GeoDataFrame(store_location_df, geometry=gpd.points_from_xy(store_location_df.longitude, store_location_df.latitude), crs='EPSG:4326')
    store_location_gdf.plot(ax=ax, markersize=store_location_gdf['2021_sales']/1000, color='red', marker='o', alpha=0.5)
    plt.title("Palmers stores location depend on 2021 sales")
    plt.show()