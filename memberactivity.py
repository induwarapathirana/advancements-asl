import streamlit as st
import pandas as pd

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

# Get unique values for the drop-down filters
entities = sorted(data.iloc[:, 1].unique())
functions = sorted(data.iloc[:, 6].unique())
durations = sorted(data.iloc[:, 8].unique())
status = sorted(data.iloc[:, 12].unique())

# Create a list of dictionaries to store record counts for each entity
entity_counts = [{'Entity': entity, 'Record Count': active_data[active_data.iloc[:, 1] == entity].shape[0]} for entity in entities]

# Display record counts for each entity in a 2-row table
st.title('Record Counts for Each Entity')
entity_counts_df = pd.DataFrame(entity_counts)
entity_counts_df = entity_counts_df.set_index('Entity').T

# Apply style to the table
entity_counts_df_styled = entity_counts_df.style\
    .set_table_styles([{'selector': 'th',
                        'props': [('background-color', 'lightblue'),
                                  ('color', 'black'),
                                  ('border', '1px solid black')]},
                       {'selector': 'td',
                        'props': [('border', '1px solid black')]}])\
    .set_properties(**{'text-align': 'center'})

# Display the styled table
st.write(entity_counts_df_styled)

# Create Streamlit filters
##st.write('### Select Entity')
selected_entity = st.selectbox('Select Entity', options=['All'] + list(entities))

##st.write('### Select Durations and Status')
col1, col2 = st.columns(2)
with col1:
    selected_duration = st.multiselect('Duration', options=durations, default=[])
with col2:    
    selected_status = st.multiselect('Status', options=status, default=[])

##st.write('### Select Functions')
selected_functions = st.multiselect('Functions', options=functions, default=[])


# Apply additional filters based on user selection
if selected_entity != 'All':
    data = data[data.iloc[:, 1] == selected_entity]
if selected_functions:
    data = data[data.iloc[:, 6].isin(selected_functions)]
if selected_duration:
    data = data[data.iloc[:, 8].isin(selected_duration)]
if selected_status:
    data = data[data.iloc[:, 12].isin(selected_status)]

# Reset index to add indexing to the DataFrame
data.reset_index(drop=True, inplace=True)
data.index += 1  # Start index from 1

# Display the filtered DataFrame with indexing
st.title('MX Realizations/Advancements')
st.write(f"Total records: {len(data)}")
st.write(data)

# Create additional visualizations or data summaries as needed
##st.line_chart(data)
##st.bar_chart(data)
