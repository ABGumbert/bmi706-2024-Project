import pandas as pd
import requests
from io import StringIO
import altair as alt
import streamlit as st

alt.data_transformers.disable_max_rows()

sorted_age_groups = ["<1 year", "1 to 4", "5 to 9", "10 to 14", "15 to 19", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40 to 44", "45 to 49", "50 to 54", "55 to 59", "60 to 64", "65 to 69", "70 to 74", "75 to 79", "80 to 84", "85 plus"]

@st.cache
def load_data_from_github(repo_owner, repo_name, file_path, branch='main'):
    """Load CSV data from a GitHub repository."""
    try:
        url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
        #print(f"Attempting to load file from: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content)
        
        #print(f"Successfully loaded {file_path} from GitHub")
        #print(f"Shape of the dataframe: {df.shape}")
        #print("\nFirst few rows of the dataframe:")
        #print(df.head())
        
        return df
    except Exception as e:
        print(f"An error occurred while loading the file: {str(e)}")
        return None

def age_group_chart(data):
    """Create a line chart of mortality rates by age group and demographic."""
    return alt.Chart(data).mark_line().encode(
        #x=alt.X('age_name:O', sort='-y', title='Age Group'),
        x=alt.X('age_name:O', sort=sorted_age_groups, title='Age Group'),
        y=alt.Y('mean(val):Q', title='Mortality Rate'),
        color=alt.Color('race_name:N', title='Racial Group'),
        tooltip=['age_name', 'race_name', 'val']
    ).properties(
        width=600,
        height=400,
        title='Mortality Rates by Age Group and Demographic'
    ).interactive()

def time_series_chart(data):
    """Create a line chart of mortality rates over time."""
    selector = alt.selection_single(fields=['sex_name', 'age_name'], bind='legend')
    
    return alt.Chart(data).mark_line().encode(
        x=alt.X('year:T', title='Year'),
        y=alt.Y('val:Q', title='Mortality Rate'),
        color='sex_name:N',
        strokeDash='age_name:N',
        tooltip=['year', 'sex_name', 'age_name', 'val']
    ).add_selection(
        selector
    ).transform_filter(
        selector
    ).properties(
        width=600,
        height=400,
        title='Mortality Rates Over Time'
    ).interactive()

def create_pivot_tables(data):
    """Create pivot tables for age, sex, and race."""
    age_pivot = data.pivot_table(values='val', index=['year', 'age_name'], aggfunc='mean').reset_index()
    sex_pivot = data.pivot_table(values='val', index=['year', 'sex_name'], aggfunc='mean').reset_index()
    race_pivot = data.pivot_table(values='val', index=['year', 'race_name'], aggfunc='mean').reset_index()
    return age_pivot, sex_pivot, race_pivot

def create_line_chart(data, category):
    """Create a line chart for a specific category."""
    return alt.Chart(data).mark_line().encode(
        x=alt.X('year:T', title='Year'),
        y=alt.Y('val:Q', title='Mortality Rate'),
        color=f'{category}:N',
        tooltip=['year', category, 'val']
    ).properties(
        width=600,
        height=400,
        title=f'Mortality Rates by {category} (2000-2019)'
    ).interactive()

def display_charts(data):
    """Display all charts based on available data."""
    st.write("Displaying charts based on available data...")
    
    st.altair_chart(age_group_chart(data), use_container_width=True)
    st.altair_chart(time_series_chart(data), use_container_width=True)
    
    age_pivot, sex_pivot, race_pivot = create_pivot_tables(data)
    st.altair_chart(create_line_chart(age_pivot, 'age_name'), use_container_width=True)
    st.altair_chart(create_line_chart(sex_pivot, 'sex_name'), use_container_width=True)
    st.altair_chart(create_line_chart(race_pivot, 'race_name'), use_container_width=True)

if __name__ == "__main__":
    repo_owner = "ABGumbert"
    repo_name = "bmi706-2024-Project"
    file_path = "Combined_USA_Data.csv"

    df = load_data_from_github(repo_owner, repo_name, file_path)

    if df is None:
        print("Data loading failed. Please check the GitHub repository details and file path.")
    else:
        #print("\nColumns in the DataFrame:")
        #print(df.columns.tolist())
        
        #print("\nData types of the columns:")
        #print(df.dtypes)
        
        #print("\nSummary statistics of numerical columns:")
        #print(df.describe())

        # Convert 'year' to datetime
        df['year'] = pd.to_datetime(df['year'], format='%Y')

        # Filter data for cirrhosis-related causes
        df_cirrhosis = df[df['cause_name'].str.contains('Cirrhosis', case=False)]

        display_charts(df_cirrhosis)
