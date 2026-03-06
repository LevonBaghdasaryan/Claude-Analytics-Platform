import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Claude Code Usage Analytics", layout="wide")

st.title("📊 Claude Code Usage Analytics Platform")
st.markdown("This dashboard provides insights into developer patterns and token consumption for Claude Code sessions.")

# 1. Database connection
@st.cache_data 
def load_data():
    conn = sqlite3.connect('claude_analytics.db')
    df = pd.read_sql('SELECT * FROM telemetry_usage', conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# 2. Sidebar (Filters)
st.sidebar.header("Filters")
practice_filter = st.sidebar.multiselect("Select Practice:", 
                                        options=df['practice'].unique(), 
                                        default=df['practice'].unique())

model_filter = st.sidebar.multiselect("Select AI Model:", 
                                     options=df['model'].unique(), 
                                     default=df['model'].unique())

# Data Filtering
filtered_df = df[(df['practice'].isin(practice_filter)) & (df['model'].isin(model_filter))]

# 3. Key Metrics (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cost ($)", f"{filtered_df['cost'].sum():,.2f}")
with col2:
    st.metric("Active Users", filtered_df['email'].nunique())
with col3:
    st.metric("Total Tokens", f"{(filtered_df['input_tokens'].sum() + filtered_df['output_tokens'].sum()):,}")
with col4:
    st.metric("Total Events", f"{len(filtered_df):,}")

st.divider()

# 4. Charts
left_col, right_col = st.columns(2)

# Chart 1: Cost by Practice
cost_by_practice = filtered_df.groupby('practice')['cost'].sum().reset_index()
fig_cost = px.bar(cost_by_practice, x='practice', y='cost', 
                 title="Total Cost by Engineering Practice", 
                 labels={'cost': 'Cost (USD)', 'practice': 'Practice'},
                 color='practice', text_auto='.2s')
left_col.plotly_chart(fig_cost, use_container_width=True)

# Chart 2: Model Distribution
model_usage = filtered_df['model'].value_counts().reset_index()
fig_model = px.pie(model_usage, values='count', names='model', 
                  title="AI Model Usage Distribution", 
                  hole=0.4)
right_col.plotly_chart(fig_model, use_container_width=True)

# Chart 3: Activity over Time
filtered_df['hour'] = filtered_df['timestamp'].dt.hour
usage_over_time = filtered_df.groupby('hour').size().reset_index(name='requests')
fig_time = px.line(usage_over_time, x='hour', y='requests', 
                  title="Peak Usage Activity (Hourly)", 
                  markers=True)
st.plotly_chart(fig_time, use_container_width=True)

# Chart 4: Top Tools
top_tools = filtered_df[filtered_df['tool_name'].notna()]['tool_name'].value_counts().head(10).reset_index()
fig_tools = px.bar(top_tools, x='count', y='tool_name', orientation='h', 
                  title="Top 10 Most Used Tools", 
                  labels={'count': 'Usage Count', 'tool_name': 'Tool Name'},
                  color='count')
st.plotly_chart(fig_tools, use_container_width=True)

# 5. Data Preview
if st.checkbox("Show Raw Telemetry Data (First 100 rows)"):
    st.dataframe(filtered_df.head(100))


from sklearn.linear_model import LinearRegression
import numpy as np

st.divider()
st.subheader("🚀 Predictive Analytics: 7-Day Cost Forecast")

# Prepare data for ML
df_ml = filtered_df.copy()
# Normalize timestamp to get only the date but keep it as datetime64 type
df_ml['date_only'] = pd.to_datetime(df_ml['timestamp'].dt.date)
daily_costs = df_ml.groupby('date_only')['cost'].sum().reset_index()

# Ensure we have enough data points (at least 5 days)
if len(daily_costs) >= 5:
    # Prepare features (X) and target (y)
    # Convert dates to numerical values (number of days from the start)
    start_date = daily_costs['date_only'].min()
    daily_costs['day_num'] = (daily_costs['date_only'] - start_date).dt.days
    
    X = daily_costs[['day_num']].values
    y = daily_costs['cost'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for the next 7 days
    last_day_num = daily_costs['day_num'].max()
    future_day_nums = np.array([[i] for i in range(last_day_num + 1, last_day_num + 8)])
    predictions = model.predict(future_day_nums)
    
    # Create forecast dataframe for plotting
    future_dates = [daily_costs['date_only'].max() + pd.Timedelta(days=i) for i in range(1, 8)]
    forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Cost': predictions})
    
    # Visualization
    fig_ml = px.line(forecast_df, x='Date', y='Predicted Cost', 
                    title="Forecasted Daily Spend (Next 7 Days)",
                    markers=True)
    fig_ml.update_traces(line_color='orange')
    fig_ml.update_layout(xaxis_title="Future Date", yaxis_title="Estimated Cost (USD)")
    st.plotly_chart(fig_ml, width="stretch")
    
    st.info(f"Based on historical data, the estimated cost for tomorrow is approximately **${max(0, predictions[0]):.2f}**.")
else:
    st.warning("Insufficient data for ML forecasting. Please ensure you have at least 5 days of usage data.")
    
#  Local URL: http://localhost:8501
#  Network URL: http://10.11.11.76:8501    