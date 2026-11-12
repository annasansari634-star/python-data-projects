import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(
    page_title="IPL Cricket Analysis",
    page_icon="🏏",
    layout="wide"
)

# --- Header ---
st.title("🏏 IPL Cricket Data Analysis")
st.markdown("Indian Premier League ke matches ka detailed interactive analysis")
st.markdown("---")

# --- File Upload ---
st.sidebar.title("📂 Data Upload")
uploaded_file = st.sidebar.file_uploader("matches.csv upload karein", type=["csv"])

# Agar file upload nahi hui, toh default path use karo
if uploaded_file is None:
    try:
        df = pd.read_csv('matches.csv')
        st.sidebar.success("✅ Local 'matches.csv' file load ho gayi")
    except FileNotFoundError:
        st.error("❌ matches.csv file nahi mili! Sidebar se upload karein ya same folder mein rakh dein.")
        st.stop()
else:
    df = pd.read_csv(uploaded_file)

# --- Data Validation ---
required_cols = {'winner', 'toss_winner'}
if not required_cols.issubset(df.columns):
    st.error(f"❌ CSV mein {required_cols} columns hone zaroori hain!")
    st.stop()

# --- Key Metrics ---
st.subheader("📊 Overview")
col1, col2, col3, col4 = st.columns(4)

total_matches = len(df)
unique_teams = df['winner'].nunique()
total_seasons = df['season'].nunique() if 'season' in df.columns else 0
top_team = df['winner'].value_counts().idxmax()

with col1:
    st.metric(label="🏟️ Total Matches", value=total_matches)
with col2:
    st.metric(label="🏆 Total Teams", value=unique_teams)
with col3:
    st.metric(label="📅 Total Seasons", value=total_seasons)
with col4:
    st.metric(label="⭐ Most Successful Team", value=top_team)

st.markdown("---")

# --- Analysis 1: Toss Winner vs Match Winner ---
st.subheader("🪙 Toss Winner vs Match Winner")
df['toss_match_same'] = df['toss_winner'] == df['winner']
toss_stats = df['toss_match_same'].value_counts()

col_t1, col_t2 = st.columns(2)

with col_t1:
    toss_win_count = toss_stats.get(True, 0)
    toss_lose_count = toss_stats.get(False, 0)
    toss_win_pct = (toss_win_count / total_matches) * 100
    
    st.metric("Toss jeetkar match jeete", f"{toss_win_count} ({toss_win_pct:.1f}%)")
    st.metric("Toss jeetkar match haare", f"{toss_lose_count} ({100-toss_win_pct:.1f}%)")

with col_t2:
    fig_toss = px.pie(
        names=['Toss Jeetkar Match Jeete', 'Toss Jeetkar Match Haare'],
        values=[toss_win_count, toss_lose_count],
        hole=0.4,
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    fig_toss.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_toss, width='stretch')

st.markdown("---")

# --- Analysis 2: Top Teams by Wins ---
st.subheader("🏆 Top Teams by Matches Won")
team_wins = df['winner'].value_counts().head(10).reset_index()
team_wins.columns = ['Team', 'Wins']

fig_teams = px.bar(
    team_wins,
    x='Team',
    y='Wins',
    color='Wins',
    color_continuous_scale='Reds',
    text='Wins'
)
fig_teams.update_layout(
    xaxis_title="Team",
    yaxis_title="Total Wins",
    margin=dict(t=20, b=80, l=20, r=20),
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_teams.update_traces(textposition='outside')
st.plotly_chart(fig_teams, width='stretch')

st.markdown("---")

# --- Analysis 3: Season-wise Trend ---
if 'season' in df.columns:
    st.subheader("📈 Matches per Season")
    season_trends = df['season'].value_counts().sort_index().reset_index()
    season_trends.columns = ['Season', 'Matches']

    fig_season = px.line(
        season_trends,
        x='Season',
        y='Matches',
        markers=True,
        color_discrete_sequence=['#3498db']
    )
    fig_season.update_traces(line=dict(width=3))
    fig_season.update_layout(
        xaxis_title="Season",
        yaxis_title="Number of Matches",
        margin=dict(t=20, b=20, l=20, r=20),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_season, width='stretch')

st.markdown("---")

# --- Data Table ---
st.subheader("📋 Raw Data Preview")
tab1, tab2 = st.tabs(["Top Teams Table", "Full Dataset"])

with tab1:
    st.dataframe(
        team_wins,
        width='stretch',
        hide_index=True
    )

with tab2:
    st.dataframe(
        df.head(50),
        width='stretch',
        hide_index=True
    )
    st.info(f"Total {len(df)} rows mein se sirf pehli 50 rows dikhayi ja rahi hain.")