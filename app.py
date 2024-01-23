import streamlit as st
import pandas as pd

# Load existing data.csv or create an empty DataFrame
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Text'])

# Streamlit app layout
st.title('Text Data Appender')
input_text = st.text_input('Enter text:')
if st.button('Submit'):
    df = pd.concat([df, pd.DataFrame({'Text': [input_text]})], ignore_index=True)
    df.to_csv('data.csv', index=False)
    st.success('Text successfully appended to data.csv!')

st.dataframe(df)
