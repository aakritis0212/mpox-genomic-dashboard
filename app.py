import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Mpox Epi Dashboard", layout="wide")
st.title("🦠 Mpox Genomic Epidemiology Dashboard")
st.markdown("An interactive tracker of pathogen genomic sequences over time.")

# 2. Data Loading & Cleaning
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("mpox_data.tsv", sep='\t')
    
    # Keep essential columns
    epi_cols = ['Accession', 'Release date', 'Geographic Location', 'Host Name']
    df = df[epi_cols]
    
    # Clean dates
    df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
    df['Year-Month'] = df['Release date'].dt.to_period('M').astype(str)
    
    # Clean locations (Splits "USA: MA" into just "USA")
    df['Country'] = df['Geographic Location'].str.split(':').str[0].str.strip()
    
    # Drop rows missing crucial mapping data
    return df.dropna(subset=['Release date', 'Country'])

df = load_and_clean_data()

# 3. Sidebar Filter
st.sidebar.header("Filter Data")
host_filter = st.sidebar.multiselect(
    "Select Host Species", 
    options=df['Host Name'].dropna().unique()
)

if host_filter:
    df = df[df['Host Name'].isin(host_filter)]

# 4. Dashboard Layout & Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Global Sequence Distribution")
    country_counts = df['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Sequence Count']
    
    fig_map = px.choropleth(
        country_counts, 
        locations="Country", 
        locationmode="country names",
        color="Sequence Count", 
        hover_name="Country", 
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("Sequencing Over Time")
    time_counts = df['Year-Month'].value_counts().reset_index().sort_values('Year-Month')
    time_counts.columns = ['Year-Month', 'Sequence Count']
    
    fig_time = px.line(
        time_counts, 
        x="Year-Month", 
        y="Sequence Count", 
        markers=True
    )
    st.plotly_chart(fig_time, use_container_width=True)
