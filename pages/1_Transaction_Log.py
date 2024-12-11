import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Transactions",
    page_icon=":table:",
    layout="wide"
)

## Working with data
st.title("Transaction Log")

# Loading Data
@st.cache_data
def load_data(path: str):
    df= pd.read_csv(path)
    df = df.drop(columns=df.columns[[0, -1, -2]])
    return df

df = load_data("./cleaned_transactions.csv")

st.dataframe(
    df, 
    column_config={
        "Date": st.column_config.DateColumn(format="MMM DD, YYYY"),
        "Amount": st.column_config.NumberColumn(format="$%.2f"),
    },
    use_container_width=True,
    height=800,   
)
