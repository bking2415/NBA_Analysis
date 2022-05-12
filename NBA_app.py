# Original Project: Dataprofessor https://github.com/dataprofessor/streamlit_freecodecamp/blob/main
# /app_3_eda_basketball/basketball_app.py
import streamlit as st
import lxml
import pandas as pd
from pandas import DataFrame
import base64
import numpy as np
# importing date class from datetime module
from datetime import date


st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple web-scraping of NBA player stats data!
* **Python libraries** 
    * *Data Analysis and Manipulation:* pandas, numpy, datetime
    * *Webpage:* base64, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# creating the date object of today's date to get the current year
current_year = date.today().year

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, current_year))))


# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    sub_player_stats = raw.drop(['Rk'], axis=1)
    return sub_player_stats


# Web scraping of all NBA player stats
@st.cache
def load_all_data(curr_year):
    all_player_stats = DataFrame()
    for year in range(1950, curr_year):
        url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
        html = pd.read_html(url, header=0)
        df = html[0]
        df['Year'] = year
        raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
        raw = raw.fillna(0)
        sub_player_stats = raw.drop(['Rk'], axis=1)
        all_player_stats = pd.concat([all_player_stats, sub_player_stats])
    return all_player_stats


player_stats = load_data(selected_year)
every_player_stats = load_all_data(current_year)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = player_stats[(player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write(
    'Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
df_selected_team = df_selected_team.astype(str)
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

#####################################
# Brandon I. King, Ph.D. Contribution
#####################################

# Scoring Leaders
if st.button('Scoring Leaders'):
    st.header('Scoring Leaders of Selected Team(s)')
    # Convert single column to int dtype.
    df_selected_team['PTS'] = df_selected_team['PTS'].astype(float)
    # Sorted Scores of the average points
    df_highest_scorers = DataFrame(
        {'Points Average': df_selected_team[['Player', 'PTS']].groupby(['Player'])['PTS'].mean()}).sort_values(by='Points Average',
                                                                                                        ascending=False).reset_index()
    df_highest_scorers.index = np.arange(1, len(df_highest_scorers) + 1)

    st.dataframe(df_highest_scorers.head())

# Assist Leaders
if st.button('Assist Leaders'):
    st.header('Assist Leaders of Selected Team(s)')
    # Convert single column to int dtype.
    df_selected_team['AST'] = df_selected_team['AST'].astype(float)
    # Sorted assists of the average assists
    df_highest_assists = DataFrame(
        {'Assist Average': df_selected_team[['Player', 'AST']].groupby(['Player'])['AST'].mean()}).sort_values(by='Assist Average',
                                                                                                        ascending=False).reset_index()
    df_highest_assists.index = np.arange(1, len(df_highest_assists) + 1)

    st.dataframe(df_highest_assists.head())

# Rebound Leaders
if st.button('Rebound Leaders'):
    st.header('Rebound Leaders of Selected Team(s)')
    # Convert single column to int dtype.
    df_selected_team['TRB'] = df_selected_team['TRB'].astype(float)
    # Sorted rebound of the rebound assists
    df_highest_rebound = DataFrame(
        {'Rebound Average': df_selected_team[['Player', 'TRB']].groupby(['Player'])['TRB'].mean()}).sort_values(by='Rebound Average',
                                                                                                       ascending=False).reset_index()
    df_highest_rebound.index = np.arange(1, len(df_highest_rebound) + 1)

    st.dataframe(df_highest_rebound.head())

# Annual Player Stats
with st.container():
    st.header('Annual Player Statistics of Selected Team(s)')
    sorted_unique_players = list(sorted(player_stats.Player.unique()))
    selected_player = st.selectbox('Players', sorted_unique_players)
    # Filtering data
    df_selected_player = every_player_stats[
            (every_player_stats.Tm.isin(selected_team)) & (every_player_stats.Pos.isin(selected_pos)) & (
                every_player_stats.Player.isin([selected_player]))]
    # Convert single column to int dtype.
    df_selected_player[['PTS', 'AST', 'TRB']] = df_selected_player[['PTS', 'AST', 'TRB']].astype(float)
    # Convert single column to str dtype.
    df_selected_player['Year'] = df_selected_player['Year'].astype(str)
    # Sorted Scores of the average points
    df_score_by_year = DataFrame(
            {'Points Average': df_selected_player[['Year', 'PTS']].groupby(['Year'])['PTS'].mean()}).reset_index()
    df_score_by_year = df_score_by_year.set_index('Year')
    df_score_by_year['Assist Average'] = df_selected_player[['Year', 'AST']].groupby(['Year'])['AST'].mean()
    df_score_by_year['Rebound Average'] = df_selected_player[['Year', 'TRB']].groupby(['Year'])['TRB'].mean()
    st.line_chart(df_score_by_year)