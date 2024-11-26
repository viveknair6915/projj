import streamlit as st
import pandas as pd
import plotly.express as px
from utilss.data_loader import load_data
import folium
from streamlit_folium import st_folium
import json  # For loading GeoJSON file

# Page Title
st.title("Exploratory Data Analysis (EDA)")

# Load Data
data = load_data()

# Sidebar Options
eda_option = st.sidebar.radio(
    "Select EDA Option:",
    ("Temporal Trends", "Correlation Matrix", "Geospatial Ananlysis")
)

# Temporal Trends Visualization
if eda_option == "Temporal Trends":
    st.subheader("Temporal Trends Visualization")
    
    # Relevant features for temporal trends
    relevant_features = [
        'cases_total', 'cases0_19',
        'cases20_99', 'NDVI_d', 'dewpoint_temperature_2m_d', 'humidity_d',
        'max_temperature_2m_d', 'min_temperature_2m_d', 'temperature_2m_d',
        'total_precipitation_d'
    ]
    
    # Ensure only relevant features from the dataset are displayed
    selectable_features = [col for col in relevant_features if col in data.columns]
    
    # Dropdown to select a feature for temporal trends
    selected_column = st.selectbox(
        "Select a column for temporal analysis:",
        options=selectable_features
    )
    
    # Slider for selecting year range
    min_year = int(data['Year'].min())
    max_year = int(data['Year'].max())
    selected_year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)  # Default range includes all years
    )
    
    # Filter data by the selected year range
    filtered_data = data[(data['Year'] >= selected_year_range[0]) & (data['Year'] <= selected_year_range[1])]
    
    if selected_column:
        # Plot using Plotly Express
        fig = px.line(
            filtered_data,
            x="Date",  # Ensure the dataset has a 'Date' column
            y=selected_column,
            title=f"Temporal Trend of {selected_column} ({selected_year_range[0]} - {selected_year_range[1]})",
            labels={selected_column: selected_column, "Date": "Date"}
        )
        fig.update_layout(xaxis_title="Date", yaxis_title=selected_column)
        st.plotly_chart(fig)
    else:
        st.warning("No relevant features available for temporal trends.")



# Correlation Matrix Visualization
elif eda_option == "Correlation Matrix":
    st.subheader("Correlation Matrix")
    
    # Predefined numeric features for correlation analysis
    predefined_features = [
        'NDVI_d', 'dewpoint_temperature_2m_d', 'humidity_d', 
        'max_temperature_2m_d', 'min_temperature_2m_d', 'temperature_2m_d',
        'surface_pressure_d', 'total_precipitation_d', 
        'Pop0_19_Urban_UF', 'PopTotal_Urban_UF', 'cases_total', 
        'max_elevation_d', 'mean_elevation_d', 'stdDev_elevation_d', 
        'ivs', 'idhm', 'renda_per_capita', 'Forest_Cover_Percent'
    ]
    
    # Ensure only the predefined features are displayed
    selectable_features = [col for col in predefined_features if col in data.columns]
    
    # Multiselect for predefined features
    selected_columns = st.multiselect(
        "Select columns for correlation analysis:",
        options=selectable_features,  # Only allow predefined features
        default=selectable_features[:5]  # Pre-select the first 5 predefined features
    )
    
    # Check if user selected columns
    if selected_columns:
        # Filter numeric columns from the predefined selection
        numeric_data = data[selected_columns]
        if numeric_data.empty:
            st.error("No numeric columns selected. Please select at least one numeric column.")
        else:
            # Compute correlation matrix
            correlation_matrix = numeric_data.corr()
            
            # Plot using Plotly Express
            fig = px.imshow(
                correlation_matrix, 
                text_auto=True, 
                title="Correlation Matrix",
                labels=dict(color="Correlation"),
                color_continuous_scale="RdBu_r",
                zmin=-1, 
                zmax=1
            )
            fig.update_layout(
                xaxis_title="Features", 
                yaxis_title="Features", 
                xaxis_tickangle=45
            )
            st.plotly_chart(fig)
    else:
        st.warning("Please select at least one column.")


elif eda_option == "Geospatial Ananlysis":
    st.subheader("Geospatial Ananlysis")


    # Load dataset
    @st.cache_data
    def load_data(file_path):
        return pd.read_csv(file_path)

# Load GeoJSON file
    @st.cache_data
    def load_geojson(geojson_path):
        with open(geojson_path, 'r') as file:
            return json.load(file)

# File paths
    # data_file = r"C:\Users\amanp\Documents\dengue_sorted.csv"
    geojson_file = r"C:\Users\amanp\Documents\brazil_geo.json"  # Update with actual path to your GeoJSON file

# Load data and GeoJSON
    # data = load_data(data_file)
    geojson_data = load_geojson(geojson_file)

# Parse date and extract year/month
    data['Year'] = pd.to_datetime(data['Date'], dayfirst=True).dt.year
    data['Month'] = pd.to_datetime(data['Date'], dayfirst=True).dt.month

# Streamlit app setup
    st.title("Geospatial Analysis of Dengue Cases in Brazil")
    st.sidebar.title("Filters")

# Year selection
    years = sorted(data['Year'].unique())
    selected_year = st.sidebar.selectbox("Select Year", years)

# Filter data by selected year
    filtered_data = data[data['Year'] == selected_year]

# Aggregate dengue cases by region (CD_UF)
    region_cases = (
        filtered_data.groupby('CD_UF')['cases_total']
        .sum()
        .reset_index()
        .rename(columns={'CD_UF': 'Region', 'cases_total': 'Total Cases'})
    )

# Mapping Brazilian state codes to abbreviations
    brazil_states = {
        11: {"name": "Rondônia", "code": "RO"}, 12: {"name": "Acre", "code": "AC"}, 13: {"name": "Amazonas", "code": "AM"},
        14: {"name": "Roraima", "code": "RR"}, 15: {"name": "Pará", "code": "PA"}, 16: {"name": "Amapá", "code": "AP"},
        17: {"name": "Tocantins", "code": "TO"}, 21: {"name": "Maranhão", "code": "MA"}, 22: {"name": "Piauí", "code": "PI"},
        23: {"name": "Ceará", "code": "CE"}, 24: {"name": "Rio Grande do Norte", "code": "RN"},
        25: {"name": "Paraíba", "code": "PB"}, 26: {"name": "Pernambuco", "code": "PE"}, 27: {"name": "Alagoas", "code": "AL"},
        28: {"name": "Sergipe", "code": "SE"}, 29: {"name": "Bahia", "code": "BA"}, 31: {"name": "Minas Gerais", "code": "MG"},
        32: {"name": "Espírito Santo", "code": "ES"}, 33: {"name": "Rio de Janeiro", "code": "RJ"},
        35: {"name": "São Paulo", "code": "SP"}, 41: {"name": "Paraná", "code": "PR"},
        42: {"name": "Santa Catarina", "code": "SC"}, 43: {"name": "Rio Grande do Sul", "code": "RS"},
        50: {"name": "Mato Grosso do Sul", "code": "MS"}, 51: {"name": "Mato Grosso", "code": "MT"},
        52: {"name": "Goiás", "code": "GO"}, 53: {"name": "Distrito Federal", "code": "DF"}
        }

# Map state numeric codes (CD_UF) to abbreviations
    state_code_to_abbreviation = {k: v["code"] for k, v in brazil_states.items()}
    region_cases['Region'] = region_cases['Region'].map(state_code_to_abbreviation)

# Folium choropleth map
    st.subheader(f"Dengue Cases in Brazil for {selected_year} (Interactive Map)")
    brazil_map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Add choropleth layer
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=region_cases,
        columns=["Region", "Total Cases"],
        key_on="feature.id",  # Matches the GeoJSON 'id' field
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Dengue Cases"
    ).add_to(brazil_map)

# Render map in Streamlit
    st_data = st_folium(brazil_map, width=700, height=500)

# Bar graph visualization
    st.subheader(f"Dengue Cases by Region in {selected_year}")
    fig = px.bar(
    region_cases,
        x='Region',
        y='Total Cases',
        color='Total Cases',
        title=f"Dengue Cases by Region ({selected_year})",
        labels={'Total Cases': 'Dengue Cases'},
        color_continuous_scale="Reds"
    )
    fig.update_layout(xaxis_title="Region", yaxis_title="Total Dengue Cases", xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Region contribution table with download option
    st.subheader("Region-Wise Dengue Cases")

# Display the table
    st.dataframe(region_cases)

# Provide a download button
    @st.cache_data
    def convert_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    # csv_data = convert_to_csv(region_cases)
    # st.download_button(
    #     label="Download Data as CSV",
    #     data=csv_data,
    #     file_name=f'dengue_cases_{selected_year}.csv',
    #     mime='text/csv'
    # )