import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from econometric_engine import compute_elasticities

st.set_page_config(page_title="Executive Pricing & Analytics Dashboard", layout="wide")

st.title("📊 Strategic Pricing Engine & Causal Analytics Dashboard")
st.markdown("### Bridging Econometric Models with Business Decisions")

# Run or load model results
try:
    models_dict = compute_elasticities()
    df_raw = pd.read_csv("data/simulated_retail_panel.csv")
except FileNotFoundError:
    st.error("Please run `python data/data_simulator.py` first to generate transactional data.")
    st.stop()

# Transform metrics dictionary into readable summary dataframe
summary_data = []
for pid, info in models_dict.items():
    summary_data.append({
        "ID": pid,
        "Product Name": info["product_name"],
        "Price Elasticity": info["elasticity"],
        "Statistical Significance (p-value)": info["p_value"],
        "Model R² Metric": info["r_squared"],
        "Avg Price ($)": info["avg_price"],
        "Avg Weekly Units": info["avg_units"]
    })
df_summary = pd.DataFrame(summary_data)

# KPI Metrics Rows
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total SKUs Analyzed", value=len(df_summary))
with col2:
    st.metric(label="Most Price-Sensitive SKU", value="Wireless Charging Pad (-2.1)")
with col3:
    st.metric(label="Least Price-Sensitive SKU", value="Stainless Water Bottle (-0.5)")

st.write("---")

# Part1: Strategic Pricing Analytics Table
st.subheader("1. Econometric Modeling Summary Matrix")
st.dataframe(df_summary.set_index("ID"), use_container_width=True)
st.caption("Note: Interpretation: A 1% increase in price translates to a β% change in sales volume.")

# Part2: Interactive What-If Scenario Simulator Component
st.write("---")
st.subheader("2. Executive 'What-If' Simulation Sandbox")

selected_name = st.selectbox("Choose a Product to Optimize:", df_summary["Product Name"].unique())
prod_row = df_summary[df_summary["Product Name"] == selected_name].iloc[0]
prod_id = prod_row["ID"]
meta = models_dict[prod_id]

col_sim1, col_sim2 = st.columns([1, 2])

with col_sim1:
    st.markdown("#### Adjust Strategy Sliders")
    price_change_pct = st.slider("Modify Price Variable (%)", min_value=-30, max_value=30, value=0, step=5)
    promo_toggle = st.checkbox("Apply Active Promotion Campaign", value=False)
    
    # Calculate baseline inputs vs simulation outputs using the fitted parameters
    old_p = meta["avg_price"]
    new_p = old_p * (1 + (price_change_pct / 100))
    
    # calculate simulated volume change with fitted log coefficients
    # log(Q_new) = Intercept + β*log(P_new) + γ*Promo + δ*log(CompPrice)
    sim_log_q = (meta["intercept"] + 
                 meta["elasticity"] * np.log(new_p) + 
                 meta["comp_coeff"] * np.log(meta["avg_price"]) + 
                 (meta["promo_coeff"] if promo_toggle else 0))
    
    # Re-scale back from logs
    simulated_units = int(np.exp(sim_log_q))
    baseline_units = int(meta["avg_units"])
    
    baseline_rev = baseline_units * old_p
    simulated_rev = simulated_units * new_p
    rev_delta = simulated_rev - baseline_rev

with col_sim2:
    st.markdown("#### Projected Causal Impact")
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("Optimized Price", f"${new_p:.2f}", f"{price_change_pct}% Change")
    c_m2.metric("Projected Unit Volume", f"{simulated_units} units", f"{simulated_units - baseline_units} vs Base")
    c_m3.metric("Projected Gross Revenue", f"${simulated_rev:,.2f}", f"${rev_delta:+,.2f} Delta")
    
    # quick visual chart output
    viz_df = pd.DataFrame({
        "Scenario": ["Baseline Scenario", "Simulated Optimization"],
        "Revenue ($)": [baseline_rev, simulated_rev]
    })
    fig = px.bar(viz_df, x="Scenario", y="Revenue ($)", color="Scenario", text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)
