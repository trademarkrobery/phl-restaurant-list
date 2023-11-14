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

# Initialize session state
if 'visited_status' not in st.session_state:
    st.session_state['visited_status'] = data['Visited'].tolist()

# Function to update session state
def update_visited_status(index, value):
    st.session_state['visited_status'][index] = value

# Streamlit app layout
st.title('Restaurant Tracker')

all, visited, not_visited = st.tabs(["All", "Visited", "Not Visited"])

with all:
    st.header("All Restaurants")
    for i, row in data.iterrows():
        # Using selectbox for each row
        visited_status = st.selectbox(f"{row['Restaurant']}, {row['Location']}, {row['Cuisine Style']}", 
                                      ["Not Visited", "Visited"], index=int(st.session_state['visited_status'][i]),
                                      key=f'selectbox_{i}')
        # Update the visited status based on selection
        new_status = True if visited_status == "Visited" else False
        if new_status != st.session_state['visited_status'][i]:
            update_visited_status(i, new_status)

with visited:
    st.header("Visited Restaurants")
    visited_restaurants = data[pd.Series(st.session_state['visited_status'])]
    st.dataframe(visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])

with not_visited:
    st.header("Not Visited Restaurants")
    not_visited_mask = ~pd.Series(st.session_state['visited_status'])
    not_visited_restaurants = data[not_visited_mask]
    st.dataframe(not_visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])