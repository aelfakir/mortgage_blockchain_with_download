import streamlit as st
import pandas as pd
import plotly.express as px
import json
#from blockchain_logic import MortgageChain

st.set_page_config(page_title="Blockchain Mortgage Ledger", layout="wide")

st.title("🏦 Blockchain Mortgage Annuity Calculator")
st.markdown("This app calculates monthly payments and stores the schedule in an immutable blockchain.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Loan Parameters")
principal = st.sidebar.number_input("Principal Amount ($)", min_value=1000, value=250000)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", 0.1, 15.0, 6.5)
years = st.sidebar.number_input("Loan Term (Years)", min_value=1, max_value=50, value=30)

# --- ANNUITY MATH ---
def calculate_annuity(P, annual_rate, years):
    r = (annual_rate / 100) / 12
    n = years * 12
    if r == 0: return P / n
    return P * (r * (1 + r)**n) / ((1 + r)**n - 1)

monthly_payment = calculate_annuity(principal, interest_rate, years)
if st.button("Generate Secure Mortgage Ledger"):
    #st.success(f"Your calculated monthly payment is ${monthly_payment:,.2f}")
    #st.subheader("Results")
    st.metric(label="Monthly Payment", value=f"${monthly_payment:,.2f}")

