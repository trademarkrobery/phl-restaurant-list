import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Google Sheets direct download link for .xlsx
url = 'https://docs.google.com/spreadsheets/d/1c16TVukKgu3aAjOUROtalXxBOkN0M825/export?format=xlsx'

# Downloading the file content
response = requests.get(url)
file = BytesIO(response.content)

# Load data, specifying the engine
data = pd.read_excel(file, engine='openpyxl')
data['Visited'] = data['Visited'].apply(lambda x: True if x == 'Yes' else False)

# Convert 'Visited' to a more user-friendly format for editing
data_for_editing = data.copy()
data_for_editing['Visited'] = data_for_editing['Visited'].apply(lambda x: "Visited" if x else "Not Visited")

# Streamlit app layout
st.title('Restaurant Tracker')

all, visited, not_visited = st.tabs(["All", "Visited", "Not Visited"])

with all:
    st.header("All Restaurants")
    # Editable DataFrame
    edited_df = st.data_editor(data_for_editing)
    
    # Reflect changes in the original data
    data['Visited'] = edited_df['Visited'] == "Visited"

with visited:
    st.header("Visited Restaurants")
    visited_restaurants = data[data['Visited']]
    st.dataframe(visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])

with not_visited:
    st.header("Not Visited Restaurants")
    not_visited_restaurants = data[~data['Visited']]
    st.dataframe(not_visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])