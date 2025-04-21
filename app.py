
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="💰 Cloud Cost Optimization", layout="wide")

# Load JSON data
with open("mock_billing.json") as f:
    raw_data = json.load(f)
df = pd.DataFrame(raw_data)
df["date"] = pd.to_datetime(df["date"])

# Sidebar Filters
st.sidebar.header("🔎 Filter")
selected_project = st.sidebar.selectbox("Project", ["All"] + sorted(df["project"].unique()))
selected_provider = st.sidebar.selectbox("Cloud Provider", ["All"] + sorted(df["cloud_provider"].unique()))

filtered_df = df.copy()
if selected_project != "All":
    filtered_df = filtered_df[filtered_df["project"] == selected_project]
if selected_provider != "All":
    filtered_df = filtered_df[filtered_df["cloud_provider"] == selected_provider]

# KPI Summary
st.title("💰 Cloud Cost Optimization Dashboard")
st.subheader("🔢 Cost Summary")
col1, col2 = st.columns(2)
col1.metric("Total Spend", f"${filtered_df['cost'].sum():,.2f}")
col2.metric("Avg CPU Utilization", f"{filtered_df['cpu_utilization'].mean() * 100:.2f}%")

# Chart: Cost by Service
st.markdown("### 📈 Cost Trend by Service")
pivot = filtered_df.pivot_table(index="date", columns="service", values="cost", aggfunc="sum")
fig, ax = plt.subplots()
pivot.plot(ax=ax, marker='o')
ax.set_ylabel("Cost ($)")
ax.set_title("Daily Cost per Service")
st.pyplot(fig)

# Optimization Recommendations
st.markdown("### 🧠 Optimization Recommendations")
recommendations = []

for _, row in filtered_df.iterrows():
    if row["cpu_utilization"] < 0.3:
        recommendations.append(f"🔻 **{row['service']}** in *{row['project']}* is underutilized. Consider downscaling or stopping.")
    if row["cost"] > 200:
        recommendations.append(f"💸 High cost alert: **{row['service']}** in *{row['project']}* is costing ${row['cost']:.2f}/day.")

if recommendations:
    for r in recommendations:
        st.write(r)
else:
    st.success("✅ All services are operating efficiently.")

# Raw Data
st.markdown("### 📄 Raw Billing Data")
st.dataframe(filtered_df)
