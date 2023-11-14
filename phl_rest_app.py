import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load data, specifying the engine
data = pd.read_excel('Restaurant_Table.xlsx', engine='openpyxl')
data['Visited'] = data['Visited'].apply(lambda x: True if x == 'Yes' else False)



# Initialize session state for visited status
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
    edited_df = st.data_editor(data, num_rows="dynamic")


with visited:
    st.header("Visited Restaurants")
    visited_restaurants = data[pd.Series(st.session_state['visited_status'])]
    st.dataframe(visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])

with not_visited:
    st.header("Not Visited Restaurants")
    not_visited_mask = ~pd.Series(st.session_state['visited_status'])
    not_visited_restaurants = data[not_visited_mask]
    st.dataframe(not_visited_restaurants[['Restaurant', 'Location', 'Cuisine Style']])