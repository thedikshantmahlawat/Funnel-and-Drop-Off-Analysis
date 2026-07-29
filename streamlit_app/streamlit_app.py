import pandas as pd
import plotly.graph_objects as go
import streamlit as st

FUNNEL_ORDER = ["home", "product_page", "cart", "checkout", "confirmation"]
STEP_LABELS = {"home": "Home", "product_page": "Product Page", "cart": "Cart",
               "checkout": "Checkout", "confirmation": "Confirmation"}

st.set_page_config(page_title="Funnel & Drop-off Analysis", page_icon="🛒", layout="wide")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, parse_dates=["Timestamp"])

df = load_data("data/processed/dim_session.csv")

st.title("🛒 E-Commerce Funnel & Drop-off Analysis")
st.caption(" → ".join(STEP_LABELS[s] for s in FUNNEL_ORDER))

st.sidebar.header("Filters")
devices = st.sidebar.multiselect("Device Type", sorted(df["DeviceType"].unique()), default=sorted(df["DeviceType"].unique()))
countries = st.sidebar.multiselect("Country", sorted(df["Country"].unique()), default=sorted(df["Country"].unique()))
referrals = st.sidebar.multiselect("Referral Source", sorted(df["ReferralSource"].unique()), default=sorted(df["ReferralSource"].unique()))

filtered = df[df["DeviceType"].isin(devices) & df["Country"].isin(countries) & df["ReferralSource"].isin(referrals)]

funnel_counts = [(filtered["MaxStepOrder"] >= i).sum() for i in range(5)]
overall_cvr = filtered["Purchased"].mean() * 100

col1, col2 = st.columns(2)
col1.metric("Sessions (filtered)", f"{len(filtered):,}")
col2.metric("Overall Conversion", f"{overall_cvr:.1f}%")

fig = go.Figure(go.Funnel(
    y=[STEP_LABELS[s] for s in FUNNEL_ORDER],
    x=funnel_counts,
    textinfo="value+percent initial",
))
st.plotly_chart(fig, use_container_width=True)