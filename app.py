import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Expense Tracker Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better UI ---
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar for File Upload ---
st.sidebar.title("📂 Data Upload")
uploaded_file = st.sidebar.file_uploader("Apna expenses.csv file yahan upload karein", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** CSV file mein `date`, `category`, aur `amount` columns hone chahiye.")

# --- Main App Logic ---
if uploaded_file is not None:
    # 1. Data Loading
    df = pd.read_csv(uploaded_file)
    
    # Basic validation
    required_cols = {'date', 'category', 'amount'}
    if not required_cols.issubset(df.columns):
        st.error(f"❌ Error: CSV file mein {required_cols} columns hone zaroori hain!")
        st.stop()

    # 2. Data Processing
    df['date'] = pd.to_datetime(df['date'])
    df['month_str'] = df['date'].dt.strftime('%Y-%m')
    
    category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    monthly_totals = df.groupby('month_str')['amount'].sum().reset_index()
    monthly_totals.columns = ['Month', 'Total Amount']

    # --- Header ---
    st.title("💸 Personal Expense Dashboard")
    st.markdown("Aapke kharchon ka ek detailed aur interactive analysis.")
    st.markdown("---")

    # --- 3. Key Metrics (Top Row) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_expense = df['amount'].sum()
    avg_monthly = monthly_totals['Total Amount'].mean()
    top_category = category_totals.idxmax()
    top_category_amount = category_totals.max()
    
    with col1:
        st.metric(label="💰 Total Expense", value=f"₹{total_expense:,.2f}")
    with col2:
        st.metric(label="📅 Average Monthly", value=f"₹{avg_monthly:,.2f}")
    with col3:
        st.metric(label="🏆 Top Category", value=top_category)
    with col4:
        st.metric(label="📊 Total Transactions", value=len(df))

    st.markdown("---")

    # --- 4. Interactive Charts ---
    chart_col1, chart_col2 = st.columns(2)

    # Colors matching your original code
    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#b3ffb3']

    with chart_col1:
        st.subheader("🥧 Where does the money go?")
        fig_pie = px.pie(
            values=category_totals.values, 
            names=category_totals.index, 
            hole=0.4, # Donut chart looks more modern
            color_discrete_sequence=custom_colors
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with chart_col2:
        st.subheader("📈 Monthly Expense Trend")
        fig_line = px.line(
            monthly_totals, 
            x='Month', 
            y='Total Amount', 
            markers=True,
            color_discrete_sequence=['#800080'] # Purple color
        )
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(
            xaxis_title="Month", 
            yaxis_title="Total Amount (₹)",
            margin=dict(t=20, b=20, l=20, r=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # --- 5. Data Tables ---
    st.markdown("---")
    st.subheader("📋 Detailed Breakdown")
    
    tab1, tab2 = st.tabs(["Category-wise Summary", "Monthly Summary"])
    
    with tab1:
        st.dataframe(
            category_totals.reset_index().rename(columns={'category': 'Category', 'amount': 'Total Spent (₹)'}),
            use_container_width=True,
            hide_index=True
        )
        
    with tab2:
        st.dataframe(
            monthly_totals.rename(columns={'Month': 'Month', 'Total Amount': 'Total Spent (₹)'}),
            use_container_width=True,
            hide_index=True
        )

else:
    # --- Welcome Screen when no file is uploaded ---
    st.info("👈 Please upload your `expenses.csv` file from the sidebar to get started.")
    
    # Show dummy data structure
    st.subheader("📝 Expected CSV Format:")
    dummy_data = {
        'date': ['2026-01-05', '2026-01-12', '2026-02-03'],
        'category': ['Food', 'Travel', 'Shopping'],
        'amount': [500, 1200, 2500]
    }
    st.dataframe(pd.DataFrame(dummy_data), use_container_width=True, hide_index=True)