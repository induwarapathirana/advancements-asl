import streamlit as st
import pandas as pd

def entity_overview(entity_counts):
    st.title('MX Realizations | LC Term 24.25')

    # Create a flexible grid layout with 3 columns
    cols = st.columns(3)
    for i, entity in enumerate(entity_counts):
        col = cols[i % 3]  # Choose the column to display the metric
        with col:
            st.metric(label=entity['Entity'], value=entity['Record Count'])
