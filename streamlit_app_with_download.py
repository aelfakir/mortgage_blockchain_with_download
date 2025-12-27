import streamlit as st
import pandas as pd
import plotly.express as px
import json
from blockchain_logic import MortgageChain

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

# --- BLOCKCHAIN GENERATION ---
if st.button("Generate Secure Mortgage Ledger"):
    my_loan_chain = MortgageChain()
    current_balance = principal
    monthly_rate = (interest_rate / 100) / 12
    
    ledger_for_display = []
    full_chain_data = [] # To store the raw block data for JSON

    for i in range(1, (years * 12) + 1):
        interest_charge = current_balance * monthly_rate
        principal_repayment = monthly_payment - interest_charge
        current_balance -= principal_repayment
        
        data = {
            "Month": i,
            "Payment": round(monthly_payment, 2),
            "Principal_Paid": round(principal_repayment, 2),
            "Interest_Paid": round(interest_charge, 2),
            "Remaining_Balance": round(max(0, current_balance), 2)
        }
        
        my_loan_chain.add_payment(data)
        
        # Capture the block for Export
        current_block = my_loan_chain.chain[-1]
        block_record = {
            "index": current_block.index,
            "hash": current_block.hash,
            "prev_hash": current_block.prev_hash,
            "timestamp": current_block.timestamp,
            "data": current_block.payment_data
        }
        full_chain_data.append(block_record)
        
        ledger_for_display.append({
            "Block_Hash": current_block.hash[:12] + "...",
            **data
        })

    df = pd.DataFrame(ledger_for_display)

    # --- UI DISPLAY & CHARTS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Payment", f"${monthly_payment:,.2f}")
    col2.metric("Total Interest", f"${(df['Interest_Paid'].sum()):,.2f}")
    col3.metric("Total Cost", f"${(monthly_payment * years * 12):,.2f}")

    st.subheader("Amortization Visualization")
    fig_split = px.line(df, x="Month", y=["Principal_Paid", "Interest_Paid"], 
                        title="Principal vs. Interest Over Time")
    st.plotly_chart(fig_split, use_container_width=True)

    # --- DOWNLOAD SECTION ---
    st.subheader("Export Blockchain Ledger")
    down_col1, down_col2 = st.columns(2)
    
    # 1. Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    down_col1.download_button(
        label="Download Ledger as CSV",
        data=csv,
        file_name='mortgage_ledger.csv',
        mime='text/csv',
    )
    
    # 2. Download as JSON (The "Real" Blockchain Data)
    json_string = json.dumps(full_chain_data, indent=4)
    down_col2.download_button(
        label="Download Blockchain as JSON",
        data=json_string,
        file_name='mortgage_blockchain.json',
        mime='application/json',
    )

    st.subheader("Immutable Blockchain Ledger View")
    st.dataframe(df, use_container_width=True)
    st.success("✅ Blockchain records ready for download.")
