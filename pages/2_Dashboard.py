import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

import constructData

st.set_page_config(
    page_title="Dashboard",
    page_icon=":Bar_Chart:",
    layout="wide"
)

# Get current date
TODAY = date.today()


st.title(f"{TODAY.strftime("%B")} Dashboard")
st.markdown(f"_Last Entry {TODAY.strftime("%D")}_")

## Monthly Spending Graph
def plot_top_left():
    monthly_budget = st.text_input("Monthly Budget: ")
    
    monthly_spending__YTD_df = constructData.monthly_spending(TODAY)
    
    fig = px.bar(
        monthly_spending__YTD_df,
        x="Month",
        y="Amount",
        title="Monthly Spending",
    )
    fig.add_hline(y=monthly_budget, line=dict(color='Green'))
    st.plotly_chart(fig)
    
## Category Pie 
def plot_bottom_left():
    category_YTD_df = constructData.category_spending(TODAY)
    
    fig = px.pie(
        category_YTD_df,
        names="Category",
        values="Amount",
        title="Spending by Category",
    )
    st.plotly_chart(fig, use_container_width=True)

## Category - Month Pivot Table 
def plot_top_right():
    (total_spent_this_month, total_spent_last_month, vs_last_month) = constructData.monthly_overview(TODAY)
    
    st.metric(f"Total Spent this Month", value=f"${total_spent_this_month:.2f}", delta=f"{vs_last_month:.1f}%", delta_color="inverse")
    st.metric(f"Total Spent last Month", value=f"${total_spent_last_month:.2f}")


## Ordering in a grid
col1, col2 = st.columns(2)

with col1:
    plot_top_left()
    plot_bottom_left()
    
with col2:
    plot_top_right()