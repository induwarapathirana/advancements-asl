import streamlit as st
import pandas as pd

def national_opps(csv_url):
    st.title('Term 2023-2024 | National Opportunities')
    
    ##@st.cache_data
    def load_and_filter_data(url, country, term):
        filtered_data = pd.DataFrame()
        chunk_size = 10000  # Adjust chunk size based on your memory constraints
        for chunk in pd.read_csv(url, chunksize=chunk_size):
            # Apply the filtering conditions
            chunk_filtered = chunk[(chunk.iloc[:, 1] == country) & 
                                   (chunk.iloc[:, 5].str.contains(term))]
            filtered_data = pd.concat([filtered_data, chunk_filtered])
        return filtered_data
    
    country = 'Sri Lanka'
    term = '2023-2024'
    
    data = load_and_filter_data(csv_url, country, term)
    
    ##st.write(data)

    # Get unique values for the drop-down filters
    entities = sorted(data.iloc[:, 1].unique())
    functions = sorted(data.iloc[:, 6].unique())
    durations = sorted(data.iloc[:, 8].unique())
    status = sorted(data.iloc[:, 12].unique())

##def national_department_filtration(data, entities, functions, durations, status):
    ##st.title('National Opportunity Realizations')
    st.write('### Select Entity')
    selected_entity = st.selectbox('Select Entity', options=[entities[0]])

    # Filter departments based on selected entity
    if selected_entity == 'All':
        filtered_data = data
        departments = sorted(data.iloc[:, 11].unique())
    else:
        filtered_data = data[data.iloc[:, 1] == selected_entity]
        departments = sorted(filtered_data.iloc[:, 11].unique())

    col1, col2 = st.columns(2)
    with col1:
        selected_duration = st.multiselect('Duration', options=durations, default=[])
    with col2:    
        selected_status = st.multiselect('Status', options=status, default=[])

    selected_functions = st.multiselect('Functions', options=functions, default=[])

    st.write('### Select Department')
    selected_department = st.selectbox('Department', options=['All'] + departments)

    # Apply additional filters based on user selection
    if selected_entity != 'All':
        data_filtered = data[data.iloc[:, 1] == selected_entity]
    else:
        data_filtered = data

    if selected_functions:
        data_filtered = data_filtered[data_filtered.iloc[:, 6].isin(selected_functions)]
    if selected_duration:
        data_filtered = data_filtered[data_filtered.iloc[:, 8].isin(selected_duration)]
    if selected_status:
        data_filtered = data_filtered[data_filtered.iloc[:, 12].isin(selected_status)]
    if selected_department != 'All':
        data_filtered = data_filtered[data_filtered.iloc[:, 11] == selected_department]

    # Get titles related to the selected department
    if selected_department != 'All':
        titles = sorted(data_filtered.iloc[:, 4].unique())
    else:
        titles = sorted(data_filtered.iloc[:, 4].unique())

    # Display titles related to the selected department
    st.write('### Titles related to the selected department')
    title_counts = [{'Title': title, 'Record Count': data_filtered[data_filtered.iloc[:, 4] == title].shape[0]} for title in titles]
    title_counts_df = pd.DataFrame(title_counts)

    # Apply style to the title table and set wider width for the Title column
    # Apply style to the title table and set wider width for the Title column
    title_counts_df_styled = title_counts_df.style\
        .set_table_styles([{'selector': 'th',
                            'props': [('background-color', 'lightblue'),
                                      ('color', 'black'),
                                      ('border', '1px solid black')]},
                           {'selector': 'td',
                            'props': [('border', '1px solid black'),
                                      ('max-width', '300px'),  # Adjust the width as needed
                                      ('white-space', 'pre-wrap'),
                                      ('word-wrap', 'break-word')]}])\
        .set_properties(subset=['Title'], **{'text-align': 'center'})

    # Display the styled title table
    st.write(title_counts_df_styled)

    # Reset index to add indexing to the DataFrame
    data_filtered.reset_index(drop=True, inplace=True)
    data_filtered.index += 1  # Start index from 1
