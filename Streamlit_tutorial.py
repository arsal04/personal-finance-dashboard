import streamlit as st
import pandas as pd

st.write("Hello, World")

# text input
x = st.text_input("Fav movie??")
st.write(x)

# buttons
is_clicked = st.button("Click Me!")
st.write(is_clicked)

## Markdown formatting
markdown_string = """
    ### this is a title
    _italics_ and **bold**
    
"""
st.write(markdown_string)


## Working with data
data = pd.read_csv("cleaned_transactions.csv")
data = data.drop(columns=data.columns[0])
st.write(data)

# Visualization
st.bar_chart(data["Category"])