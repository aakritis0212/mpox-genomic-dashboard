# mpox-genomic-dashboard
# 🦠 Genomic Epidemiology Dashboard

An interactive web application built with Python, Streamlit, and Plotly to track and visualize the global distribution of viral genomic sequences over time. 

## 📊 Overview
Genomic surveillance is critical for understanding pathogen spread. This dashboard automates the pipeline from raw NIH database queries to interactive public health visualizations, allowing users to filter sequence data by host species and instantly see geographic and temporal footprints.

**Built for:** Exploring real-world epidemiological metadata extracted directly from NCBI.

## 🛠️ Tech Stack
* **Data Extraction:** NCBI Datasets CLI (`ncbi-datasets-cli`)
* **Data Processing:** Python, Pandas (Datetime standardisation, string parsing)
* **Web Framework:** Streamlit
* **Visualization:** Plotly Express (Choropleth maps, reactive line charts)

## 🚀 The Data Pipeline
1. **Raw Metadata Retrieval:** Queried `12,700+` Mpox sequence records via the NCBI Datasets CLI in JSONL format.
2. **Tabular Conversion:** Converted to TSV using NCBI dataformat tools.
3. **Data Cleaning:** Handled in Pandas to strip `NaN` values, standardize country formats, and convert strings to actionable datetime objects.
4. **UI/UX:** Streamlit caching (`@st.cache_data`) implemented for fast, reactive chart rendering.

## 💻 How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install streamlit plotly pandas`
3. Launch the app: `streamlit run app.py`
