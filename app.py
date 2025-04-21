import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="💡 Cloud Cost Estimator", layout="wide")
st.title("💡 Interactive Cloud Cost Estimator")
st.caption("Plan, visualize, and optimize cloud infrastructure based on your workload.")

# ---------------------------
# Cloud Pricing Reference
# ---------------------------
RATES = {
    "AWS":    {"cpu_hr": 0.01,   "ram_hr": 0.005,  "storage_gb_mo": 0.10,  "req_cost": 0.001},
    "GCP":    {"cpu_hr": 0.009,  "ram_hr": 0.0045, "storage_gb_mo": 0.09,  "req_cost": 0.0009},
    "Azure":  {"cpu_hr": 0.011,  "ram_hr": 0.0055, "storage_gb_mo": 0.11,  "req_cost": 0.0011}
}

# ---------------------------
# Sidebar Inputs
# ---------------------------
st.sidebar.header("🛠️ Configuration")
provider = st.sidebar.radio("Select Cloud Provider", ["AWS", "GCP", "Azure"], horizontal=True)

st.sidebar.markdown("### 🧮 Resource Settings")
cpu = st.sidebar.slider("🧠 vCPUs", 1, 64, 4)
ram = st.sidebar.slider("💾 RAM (GB)", 1, 256, 16)
storage = st.sidebar.slider("🗄️ Storage (GB)", 10, 2000, 100)

st.sidebar.markdown("### 👥 User Traffic Simulation")
users = st.sidebar.number_input("👤 Number of Users", 10, 100000, 500)
frequency = st.sidebar.selectbox("📈 Request Frequency", ["per minute", "per hour", "per day"])
usage_type = st.sidebar.selectbox("🕒 Environment", ["Production", "Development"])
duration_days = st.sidebar.slider("📅 Duration (days)", 1, 31, 30)

# ---------------------------
# Usage & Cost Calculation
# ---------------------------
hours = duration_days * 24
if frequency == "per minute":
    total_requests = users * 60 * hours
elif frequency == "per hour":
    total_requests = users * hours
else:
    total_requests = users * duration_days

rate = RATES[provider]
cpu_cost = cpu * rate["cpu_hr"] * hours
ram_cost = ram * rate["ram_hr"] * hours
storage_cost = storage * rate["storage_gb_mo"]
request_cost = total_requests * rate["req_cost"]
total_cost = cpu_cost + ram_cost + storage_cost + request_cost

if usage_type == "Development":
    total_cost *= 0.7  # apply 30% discount for dev env (assume spot/savings)

# ---------------------------
# Main Summary
# ---------------------------
st.subheader("💵 Estimated Cloud Cost Summary")
col1, col2 = st.columns(2)
col1.metric("📦 Total Monthly Cost", f"${total_cost:,.2f}")
col2.metric("📨 Estimated Requests", f"{total_requests:,}")

st.progress(min(1.0, total_cost / 500))  # visual progress indicator

# ---------------------------
# Cost Breakdown Bar Chart
# ---------------------------
st.markdown("### 📊 Cost Breakdown (in USD)")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

cost_data = pd.DataFrame({
    "Component": ["CPU", "RAM", "Storage", "Requests"],
    "Cost (USD)": [cpu_cost, ram_cost, storage_cost, request_cost]
})

fig, ax = plt.subplots(figsize=(8, 4))
bars = sns.barplot(data=cost_data, x="Cost (USD)", y="Component", ax=ax)
ax.set_title("Component-wise Cloud Cost")
ax.bar_label(bars.containers[0], fmt="$%.2f")
st.pyplot(fig)

# ---------------------------
# Optimization Feedback
# ---------------------------
st.markdown("### 🧠 Optimization Suggestions")
tips = []

if cpu_cost > 100:
    tips.append("🧠 **High CPU cost** – consider using burstable or ARM-based instances.")
if ram_cost > 50 and ram / cpu > 4:
    tips.append("💡 You're allocating a lot of RAM per vCPU. Consider lowering memory or switching to memory-optimized plans only if justified.")
if request_cost > 200:
    tips.append("📉 **Request volume is high** – consider using caching, static CDN content, or load throttling.")
if storage > 1000:
    tips.append("🗃️ **Large storage** – consider lifecycle rules or object archival (e.g., S3 Glacier).")

if tips:
    for tip in tips:
        st.markdown(f"- {tip}")
else:
    st.success("✅ Your current setup looks cost-efficient!")

with st.expander("📘 Advanced Tip"):
    st.info("""
    For **dev environments**, consider spot instances, preemptible VMs, or serverless options like AWS Lambda to further reduce costs.
    """)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("🔍 Built for startups, engineers, and cost-conscious teams.")
