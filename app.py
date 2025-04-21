import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="💡 Cloud Cost Estimator", layout="wide")
st.title("💡 Interactive Cloud Cost Estimator")
st.caption("Estimate cloud spend and get optimization suggestions based on your usage.")

# ---------------------------
# Constants (simplified rates)
# ---------------------------
RATES = {
    "AWS": {"cpu_hr": 0.01, "ram_hr": 0.005, "storage_gb_mo": 0.10, "req_cost": 0.001},
    "GCP": {"cpu_hr": 0.009, "ram_hr": 0.0045, "storage_gb_mo": 0.09, "req_cost": 0.0009},
    "Azure": {"cpu_hr": 0.011, "ram_hr": 0.0055, "storage_gb_mo": 0.11, "req_cost": 0.0011}
}

# ---------------------------
# User Inputs
# ---------------------------
st.sidebar.header("📥 Your Configuration")

provider = st.sidebar.selectbox("Cloud Provider", ["AWS", "GCP", "Azure"])
cpu = st.sidebar.slider("vCPUs", 1, 64, 4)
ram = st.sidebar.slider("RAM (GB)", 1, 256, 16)
storage = st.sidebar.slider("Storage (GB)", 10, 2000, 100)
users = st.sidebar.number_input("Users", 10, 100000, 500)
frequency = st.sidebar.selectbox("Request Frequency", ["per minute", "per hour", "per day"])
duration_days = st.sidebar.slider("Usage Duration (days/month)", 1, 31, 30)

# ---------------------------
# Calculate Usage
# ---------------------------
hours = duration_days * 24
if frequency == "per minute":
    total_requests = users * 60 * hours
elif frequency == "per hour":
    total_requests = users * hours
else:
    total_requests = users * duration_days

# Pricing
rate = RATES[provider]
cpu_cost = cpu * rate["cpu_hr"] * hours
ram_cost = ram * rate["ram_hr"] * hours
storage_cost = storage * rate["storage_gb_mo"]
request_cost = total_requests * rate["req_cost"]
total_cost = cpu_cost + ram_cost + storage_cost + request_cost

# ---------------------------
# Output Summary
# ---------------------------
st.header("📊 Estimated Monthly Cost")
col1, col2 = st.columns(2)
col1.metric("💵 Total Cost", f"${total_cost:,.2f}")
col2.metric("📨 Requests Estimated", f"{total_requests:,}")

# ---------------------------
# Cost Breakdown Chart
# ---------------------------
st.markdown("### 🧾 Cost Breakdown")
labels = ["CPU", "RAM", "Storage", "Request Load"]
values = [cpu_cost, ram_cost, storage_cost, request_cost]
fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
ax.axis("equal")
st.pyplot(fig)

# ---------------------------
# Optimization Tips
# ---------------------------
st.markdown("### 🧠 Optimization Suggestions")
tips = []

if cpu_cost > 100:
    tips.append("🔻 Consider reducing vCPU or using burstable instances.")
if ram_cost > 50 and ram / cpu > 4:
    tips.append("💡 You might be over-allocating RAM relative to CPU.")
if request_cost > 200:
    tips.append("📉 Use caching or CDN to reduce frequent backend hits.")
if storage_cost > 50 and storage > 1000:
    tips.append("🧹 Archive cold data to cheaper storage tiers (e.g., S3 Glacier).")

if tips:
    for tip in tips:
        st.write(tip)
else:
    st.success("✅ Your configuration looks optimized!")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("Built with ❤️ for cloud planning and budgeting.")
