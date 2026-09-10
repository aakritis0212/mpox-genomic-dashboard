import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Mpox Genomic Surveillance Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 Mpox Genomic Surveillance & Epidemiology Dashboard")
st.markdown("Tracking global mpox lineages, geographic spread, and clade distributions using public surveillance data.")

# Load dataset
@st.cache_data
def load_data():
    data = {
        'Accession': ['MT123456', 'MT123457', 'MT123458', 'MT123459', 'MT123460', 'MT123461'],
        'Country': ['USA', 'UK', 'Germany', 'Brazil', 'Canada', 'Democratic Republic of Congo'],
        'Clade': ['Clade IIb', 'Clade IIb', 'Clade IIb', 'Clade I', 'Clade IIb', 'Clade I'],
        'Collection_Date': ['2024-05-10', '2024-05-12', '2024-06-01', '2024-06-15', '2024-07-01', '2024-07-10'],
        'Latitude': [37.0902, 55.3781, 51.1657, -14.2350, 56.1303, -4.0383],
        'Longitude': [-95.7129, -3.4360, 10.4515, -51.9253, -106.3468, 21.7587],
        'Sequence_Count': [5200, 1800, 2100, 950, 1200, 3100]
    }
    df = pd.DataFrame(data)
    df['Collection_Date'] = pd.to_datetime(df['Collection_Date'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Surveillance Data")
selected_clade = st.sidebar.selectbox("Select Clade", options=["All"] + list(df['Clade'].unique()))

if selected_clade != "All":
    filtered_df = df[df['Clade'] == selected_clade]
else:
    filtered_df = df

# Main Layout Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Records Tracked", len(filtered_df))
col2.metric("Countries Impacted", filtered_df['Country'].nunique())
col3.metric("Dominant Lineage", filtered_df['Clade'].mode()[0] if not filtered_df.empty else "N/A")

st.markdown("---")

# Two-column layout for charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Temporal Trend")
    if not filtered_df.empty:
        timeline_df = filtered_df.groupby('Collection_Date')['Sequence_Count'].sum().reset_index()
        fig_time = px.line(timeline_df, x='Collection_Date', y='Sequence_Count', markers=True, title="Sequencing Volume Over Time")
        st.plotly_chart(fig_time, use_container_width=True)

with chart_col2:
    st.subheader("🧬 Clade Distribution")
    if not filtered_df.empty:
        clade_counts = filtered_df['Clade'].value_counts().reset_index()
        clade_counts.columns = ['Clade', 'Count']
        fig_pie = px.pie(clade_counts, names='Clade', values='Count', hole=0.4, title="Proportion by Clade")
        st.plotly_chart(fig_pie, use_container_width=True)

# Geographic Map Visualization
st.subheader("🌍 Global Geographic Distribution")
if not filtered_df.empty:
    fig_map = px.scatter_map(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        size="Sequence_Count",
        hover_name="Country",
        hover_data=["Accession", "Clade", "Collection_Date"],
        color="Clade",
        zoom=1,
        height=450
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("No data available for the selected filter.")

# Data Table View
st.subheader("📋 Raw Metadata Inspector")
st.dataframe(filtered_df, use_container_width=True)



