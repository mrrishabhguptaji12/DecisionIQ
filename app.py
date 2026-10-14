import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="DecisionIQ", layout="wide")
st.title("DecisionIQ — Business Insights Demo")
st.caption("Synthetic demonstration data; replace with a properly licensed dataset before portfolio publication.")

@st.cache_data
def load_data():
    rng = np.random.default_rng(7)
    n = 500
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    units = rng.integers(1, 25, n)
    price = rng.uniform(15, 180, n).round(2)
    cost = (price * rng.uniform(.45, .85, n)).round(2)
    return pd.DataFrame({
        "date": dates,
        "region": rng.choice(["North", "South", "East", "West"], n),
        "category": rng.choice(["Home", "Electronics", "Beauty", "Sports"], n),
        "units": units, "price": price, "unit_cost": cost
    }).assign(revenue=lambda d: d.units*d.price,
              profit=lambda d: d.units*(d.price-d.unit_cost))

df = load_data()
regions = st.multiselect("Region", sorted(df.region.unique()), default=sorted(df.region.unique()))
df = df[df.region.isin(regions)]
revenue = df.revenue.sum()
profit = df.profit.sum()
margin = profit / revenue if revenue else 0
a,b,c,d = st.columns(4)
a.metric("Revenue", f"${revenue:,.0f}")
b.metric("Profit", f"${profit:,.0f}")
c.metric("Profit margin", f"{margin:.1%}")
d.metric("Orders", f"{len(df):,}")
left,right = st.columns(2)
with left:
    st.plotly_chart(px.line(df.groupby("date", as_index=False).revenue.sum(), x="date", y="revenue", title="Daily Revenue"), use_container_width=True)
with right:
    st.plotly_chart(px.bar(df.groupby("category", as_index=False).profit.sum(), x="category", y="profit", title="Profit by Category"), use_container_width=True)
st.subheader("What-if scenario")
price_change = st.slider("Price change (%)", -20, 20, 0)
cost_change = st.slider("Unit cost change (%)", -20, 20, 0)
scenario_revenue = (df.units * df.price * (1+price_change/100)).sum()
scenario_cost = (df.units * df.unit_cost * (1+cost_change/100)).sum()
st.write({"Scenario revenue": round(float(scenario_revenue),2),
          "Scenario profit": round(float(scenario_revenue-scenario_cost),2)})
st.download_button("Download filtered data", df.to_csv(index=False), "decisioniq_demo.csv", "text/csv")
