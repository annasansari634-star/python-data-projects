import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(
    page_title="Mumbai Weather Analysis",
    page_icon="🌦️",
    layout="wide"
)

# --- Header ---
st.title("🌦️ Mumbai Weather Analysis Dashboard")
st.markdown("Mumbai ke temperature ka detailed interactive analysis")
st.markdown("---")

# --- File Upload ---
st.sidebar.title("📂 Data Upload")
uploaded_file = st.sidebar.file_uploader("Mumbai_weather.csv upload karein", type=["csv"])

# Agar file upload nahi hui, toh default path use karo
if uploaded_file is None:
    try:
        df = pd.read_csv('Mumbai_weather.csv')
        st.sidebar.success("✅ Local 'Mumbai_weather.csv' load ho gayi")
    except FileNotFoundError:
        st.error("❌ Mumbai_weather.csv file nahi mili! Sidebar se upload karein ya same folder mein rakh dein.")
        st.stop()
else:
    df = pd.read_csv(uploaded_file)

# --- Data Validation ---
if 'DATE' not in df.columns or 'T2M' not in df.columns:
    st.error("❌ CSV mein 'DATE' aur 'T2M' columns hone zaroori hain!")
    st.stop()

# --- Data Cleaning ---
try:
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')
except:
    df['DATE'] = pd.to_datetime(df['DATE'])

df = df.sort_values('DATE')
df.set_index('DATE', inplace=True)
df['T2M'] = df['T2M'].ffill()

# --- Rolling Average ---
df['Temp_Rolling_30d'] = df['T2M'].rolling(window=30).mean()

# --- Extra columns for analysis ---
df['Month'] = df.index.month
df['Year'] = df.index.year
df['Month_Name'] = df.index.strftime('%b')

# --- Key Metrics ---
st.subheader("📊 Overview")
col1, col2, col3, col4 = st.columns(4)

avg_temp = df['T2M'].mean()
max_temp = df['T2M'].max()
min_temp = df['T2M'].min()
data_years = df.index.year.nunique()

with col1:
    st.metric(label="🌡️ Average Temperature", value=f"{avg_temp:.2f}°C")
with col2:
    st.metric(label="🔥 Hottest Day", value=f"{max_temp:.2f}°C")
with col3:
    st.metric(label="❄️ Coldest Day", value=f"{min_temp:.2f}°C")
with col4:
    st.metric(label="📅 Years of Data", value=data_years)

st.markdown("---")

# --- Main Chart: Daily vs Rolling Average ---
st.subheader("📈 Temperature Trend (Daily vs 30-Day Rolling Average)")

fig_trend = go.Figure()

fig_trend.add_trace(go.Scatter(
    x=df.index,
    y=df['T2M'],
    mode='lines',
    name='Daily Temperature (T2M)',
    line=dict(color='#a6c8e0', width=1),
    opacity=0.5
))

fig_trend.add_trace(go.Scatter(
    x=df.index,
    y=df['Temp_Rolling_30d'],
    mode='lines',
    name='30-Day Rolling Average',
    line=dict(color='#d9534f', width=3)
))

fig_trend.update_layout(
    xaxis_title="Year",
    yaxis_title="Temperature (°C)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=40, b=40, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified'
)
st.plotly_chart(fig_trend, width='stretch')

st.markdown("---")

# --- Monthly Average Analysis ---
st.subheader("📅 Monthly Average Temperature")

monthly_avg = df.groupby('Month_Name')['T2M'].mean()
# Order months properly
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_avg = monthly_avg.reindex(month_order).dropna().reset_index()
monthly_avg.columns = ['Month', 'Avg Temperature']

fig_monthly = px.bar(
    monthly_avg,
    x='Month',
    y='Avg Temperature',
    color='Avg Temperature',
    color_continuous_scale='RdYlBu_r',
    text=monthly_avg['Avg Temperature'].apply(lambda x: f'{x:.1f}°C')
)
fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Temperature (°C)",
    margin=dict(t=20, b=40, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_monthly.update_traces(textposition='outside')
st.plotly_chart(fig_monthly, width='stretch')

st.markdown("---")

# --- Seasonal Analysis (Mumbai specific) ---
st.subheader("🌴 Seasonal Temperature Analysis")

def get_season(month):
    if month in [3, 4, 5]:
        return '☀️ Summer (Mar-May)'
    elif month in [6, 7, 8, 9]:
        return '🌧️ Monsoon (Jun-Sep)'
    elif month in [10, 11]:
        return '🍂 Post-Monsoon (Oct-Nov)'
    else:
        return '❄️ Winter (Dec-Feb)'

df['Season'] = df['Month'].apply(get_season)
seasonal_avg = df.groupby('Season')['T2M'].mean().reset_index()
seasonal_avg.columns = ['Season', 'Avg Temperature']

# Custom order
season_order = ['❄️ Winter (Dec-Feb)', '☀️ Summer (Mar-May)', '🌧️ Monsoon (Jun-Sep)', '🍂 Post-Monsoon (Oct-Nov)']
seasonal_avg['Season'] = pd.Categorical(seasonal_avg['Season'], categories=season_order, ordered=True)
seasonal_avg = seasonal_avg.sort_values('Season')

fig_season = px.bar(
    seasonal_avg,
    x='Season',
    y='Avg Temperature',
    color='Season',
    color_discrete_map={
        '❄️ Winter (Dec-Feb)': '#3498db',
        '☀️ Summer (Mar-May)': '#e74c3c',
        '🌧️ Monsoon (Jun-Sep)': '#27ae60',
        '🍂 Post-Monsoon (Oct-Nov)': '#f39c12'
    },
    text=seasonal_avg['Avg Temperature'].apply(lambda x: f'{x:.1f}°C')
)
fig_season.update_layout(
    xaxis_title="Season",
    yaxis_title="Average Temperature (°C)",
    showlegend=False,
    margin=dict(t=20, b=40, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_season.update_traces(textposition='outside')
st.plotly_chart(fig_season, width='stretch')

st.markdown("---")

# --- Yearly Trend ---
st.subheader("📊 Yearly Average Temperature")

yearly_avg = df.groupby('Year')['T2M'].mean().reset_index()
yearly_avg.columns = ['Year', 'Avg Temperature']

fig_yearly = px.line(
    yearly_avg,
    x='Year',
    y='Avg Temperature',
    markers=True,
    color_discrete_sequence=['#9b59b6']
)
fig_yearly.update_traces(line=dict(width=3))
fig_yearly.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Temperature (°C)",
    margin=dict(t=20, b=40, l=40, r=40),
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_yearly, width='stretch')

st.markdown("---")

# --- Data Table ---
st.subheader("📋 Raw Data Preview")
tab1, tab2 = st.tabs(["Summary Tables", "Full Dataset"])

with tab1:
    st.write("**Monthly Averages:**")
    st.dataframe(monthly_avg, width='stretch', hide_index=True)
    
    st.write("**Seasonal Averages:**")
    st.dataframe(seasonal_avg, width='stretch', hide_index=True)

with tab2:
    st.dataframe(
        df.reset_index().head(50),
        width='stretch',
        hide_index=True
    )
    st.info(f"Total {len(df)} rows mein se sirf pehli 50 rows dikhayi ja rahi hain.")