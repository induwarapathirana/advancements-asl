import streamlit as st
import pandas as pd
from entity_overview import entity_overview
from department_filtration import department_filtration

# URL of the CSV file in Google Drive
csv_url = 'https://drive.google.com/uc?export=download&id=1DGIRK6IGibZB4wtYwgsQRx5o5IlxdLnp'

# Load and filter the CSV file in chunks
@st.cache_data
def load_and_filter_data(url, country, term):
    filtered_data = pd.DataFrame()
    chunk_size = 10000  # Adjust chunk size based on your memory constraints
    for chunk in pd.read_csv(url, chunksize=chunk_size):
        # Apply the filtering conditions
        chunk_filtered = chunk[(chunk.iloc[:, 2] == country) & 
                               (chunk.iloc[:, 5].str.contains(term))]
        filtered_data = pd.concat([filtered_data, chunk_filtered])
    return filtered_data

# Parameters for initial filtering
country = 'Sri Lanka'
term = '2024-2025'

# Load and filter data
data = load_and_filter_data(csv_url, country, term)

# Filter data for only active status
active_data = data[data.iloc[:, 12] == 'Active Role']

# Convert department column to strings and sort them alphabetically
data.iloc[:, 11] = data.iloc[:, 11].astype(str)

# Get unique values for the drop-down filters
entities = sorted(data.iloc[:, 1].unique())
functions = sorted(data.iloc[:, 6].unique())
durations = sorted(data.iloc[:, 8].unique())
status = sorted(data.iloc[:, 12].unique())

# Create a list of dictionaries to store record counts for each entity
entity_counts = [{'Entity': entity, 'Record Count': active_data[active_data.iloc[:, 1] == entity].shape[0]} for entity in entities]

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Entity Overview", "Department Filtration"])

if page == "Entity Overview":
    entity_overview(entity_counts)
elif page == "Department Filtration":
    department_filtration(data, entities, functions, durations, status)
