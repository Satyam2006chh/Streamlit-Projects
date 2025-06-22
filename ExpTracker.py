import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


st.set_page_config(page_title = "Expense Tracker", layout = "wide")
st.title("💰 Personal Expense Tracker 💰")

with st.sidebar:
    st.header("➕Add Expense➕")
    date = st.date_input("Date", datetime.today())

    category = st.selectbox("Enter the Category of Expense: ", ["Food","Transportation","Clothes","Rent"])
    if category:
        st.success(f"You selected {category} for the Expense !")
    amount = st.number_input("Enter the Amount: ", min_value=1.00,format="%.2f")
    description = st.text_input("Enter Description for Expense:")

    



