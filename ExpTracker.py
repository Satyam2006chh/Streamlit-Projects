import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Personal Expense Tracker 💰")

with st.sidebar:
    st.header("➕ Add Expense ➕")
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Enter the Category of Expense:", ["Food", "Transportation", "Clothes", "Rent"])
    
    if category:
        st.success(f"You selected {category} for the Expense!")
    
    amount = st.number_input("Enter the Amount:", min_value=1.00, format="%.2f")
    description = st.text_input("Enter Description for Expense:")

    if st.button("Add Expense"):
        if amount <= 1.00:
            st.warning("Amount must be greater than ₹1.00")
        else:
            new_expense = {
                "Date": date,
                "Category": category,
                "Amount": amount,
                "Description": description
            }
            st.session_state.expenses.append(new_expense)
            st.success("Expense Added")

df = pd.DataFrame(st.session_state.expenses)

if not df.empty:
    st.subheader("📋 Expense History")
    st.dataframe(df)

    total = df["Amount"].sum()
    st.metric("Total Spent", f"₹{total:.2f}")

    st.subheader("📊 Spending by Category")
    category_data = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.bar(category_data.index, category_data.values, color='black')
    ax.set_ylabel("Spent")
    ax.set_title("Expense by Category")
    st.pyplot(fig)
else:
    st.info("No expenses yet. Add some from the sidebar.")
