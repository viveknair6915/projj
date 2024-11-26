import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
# -1: 'Rondônia',
# DEP_NAMES mapping the numeric codes to state names
DEP_NAMES = {
     0: 'Acre', 1: 'Amazonas', 2: 'Roraima', 3: 'Pará', 4: 'Amapá',
    5: 'Tocantins', 6: 'Maranhão', 7: 'Piauí', 8: 'Ceará', 9: 'Rio Grande do Norte',
    10: 'Paraíba', 11: 'Pernambuco', 12: 'Alagoas', 13: 'Sergipe', 14: 'Bahia',
    15: 'Minas Gerais', 16: 'Espírito Santo', 17: 'Rio de Janeiro', 18: 'São Paulo',
    19: 'Paraná', 20: 'Santa Catarina', 21: 'Rio Grande do Sul', 22: 'Mato Grosso do Sul',
    23: 'Mato Grosso', 24: 'Goiás', 25: 'Distrito Federal'
}

def plot_temporal_trends(data):
    """Plots a bar chart of dengue cases over time.

    Args:
        data: A pandas DataFrame containing the data.

    Returns:
        A matplotlib figure object.
    """

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(data['Month'], data['cases_total'])
    ax.set_title("Temporal Trends")
    ax.set_xlabel("Month")
    ax.set_ylabel("Dengue Cases")
    return fig

def plot_correlation_heatmap(data, selected_features=None):
    # Select only the features you care about (if provided)
    
    if selected_features:
        data_numeric = data[selected_features]
    else:
        data_numeric = data.select_dtypes(include=[float, int])

    # Calculate the correlation matrix
    corr = data_numeric.corr()

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    return fig


def plot_geospatial_choropleth(dengue_data, geojson_path=None):
    """
    Plots a choropleth map showing dengue cases across Brazilian regions or states.
    
    Parameters:
    - dengue_data (str or DataFrame): Path to the CSV file or a DataFrame containing dengue data with regions/states. 
    - geojson_path (str, optional): Path to a GeoJSON file with geographical boundaries for Brazilian states.
    
    Returns:
    - Matplotlib figure: Choropleth map figure.
    """
    # Load your dengue data (either from CSV or DataFrame)
    if isinstance(dengue_data, str):
        data = pd.read_csv(dengue_data)
    else:
        data = dengue_data
    
    # Map the numeric state codes to names using the DEP_NAMES dictionary
    data['region'] = data['CD_UF'].map(DEP_NAMES)  # Add a new column 'region' with state names

    # If a GeoJSON file is provided, use it to load Brazilian state boundaries
    if geojson_path:
        # Load GeoJSON file (Brazilian states)
        gdf = gpd.read_file(geojson_path)
        # Merge the geospatial data with your dengue data using the state names
        gdf = gdf.merge(data, left_on='sigla', right_on='region', how='left')  # Merge by state name
    else:
        # Load the Natural Earth dataset for countries
        world = gpd.read_file("C:/Users/amanp/Desktop/MINOR/proj/code/dataset/ne_110m_admin_0_countries.shp")  # Path to the downloaded shapefile
        # Filter Brazil
        brazil = world[world['NAME'] == 'Brazil']
        # Merge the data with the world dataset using the correct column names
        brazil = brazil.merge(data, left_on='NAME', right_on='region', how='left')  # Merge by state name
        gdf = brazil
    
    # Ensure 'cases_total' is numeric, and fill any NaN values
    gdf['cases_total'] = pd.to_numeric(gdf['cases_total'], errors='coerce')
    gdf = gdf.fillna({'cases_total': 0})  # Replace NaN with 0 in 'cases_total'
    
    # Check if the 'geometry' column is valid
    if gdf.geometry.isnull().any():
        print("Warning: There are invalid geometries in the data.")
        gdf = gdf.dropna(subset=['geometry'])  # Drop rows with invalid geometries

    # Plot the choropleth map with varied color based on cases_total
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Plot the map with varied color (using cases_total as the value for coloring)
    gdf.plot(column='cases_total', cmap='YlOrRd', legend=True, ax=ax, 
             legend_kwds={'label': "Total Dengue Cases", 'orientation': "horizontal"},
             edgecolor='black', linewidth=1)  # Distinguish state borders with black edges
    
    # Add state names to each region (state) in the map
    for idx, row in gdf.iterrows():
        state_name = row['region']
        # Get the centroid for each state
        x, y = row['geometry'].centroid.coords[0]
        ax.text(x, y, state_name, fontsize=8, ha='center', color='black', fontweight='bold')

    # Set the aspect ratio and plot title
    ax.set_aspect('auto')  # Automatically adjusts the aspect ratio
    ax.set_title('Geospatial Dengue Cases')
    plt.show()

    return fig
    
    



def plot_actual_vs_predicted(predictions_file, actual_data):
    pred = pd.read_csv(predictions_file)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(actual_data['Date'], actual_data['cases_total'], label="Actual")
    ax.plot(pred['Date'], pred['cases_total'], label="Predicted")
    ax.legend()
    return fig

# Add additional visualization functions here
